import os
import shutil
import uuid
import uvicorn
import boto3

from fastapi import FastAPI, UploadFile, File

from fastsam import FastSAM, FastSAMPrompt

app = FastAPI()

model = FastSAM('assets/FastSAM-x.pt')
DEVICE = 'cpu'


s3_client = boto3.client(
    's3',
    endpoint_url=os.getenv('MINIO_ENDPOINT'),
    aws_access_key_id=os.getenv('MINIO_ROOT_USER'),
    aws_secret_access_key=os.getenv('MINIO_ROOT_PASSWORD'),
    verify=False
)
BUCKET_NAME = os.getenv('MINIO_BUCKET_NAME')


@app.post("/segment")
async def segment_image(
    file: UploadFile = File(...),
    prompt: str = "a white dog",
    conf: float = 0.4,
    iou: float = 0.9,
):
    os.makedirs("temp_inputs", exist_ok=True)
    os.makedirs("temp_outputs", exist_ok=True)

    input_filename = f"{uuid.uuid4()}{os.path.splitext(file.filename)[1]}"
    output_filename = f"result_{uuid.uuid4()}.jpg"

    input_path = f"temp_inputs/{input_filename}"
    output_path = f"temp_outputs/{output_filename}"

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    everything_results = model(
        input_path,
        device=DEVICE,
        retina_masks=True,
        imgsz=1024,
        conf=conf,
        iou=iou,
    )

    prompt_process = FastSAMPrompt(
        input_path,
        everything_results,
        device=DEVICE,
    )

    ann = prompt_process.text_prompt(prompt)

    prompt_process.plot(annotations=ann, output_path=output_path)

    with open(output_path, "rb") as file:
        s3_client.upload_fileobj(
            file,
            BUCKET_NAME,
            output_filename,
            ExtraArgs={'ContentType': 'image/jpeg'}
        )

    url = s3_client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': BUCKET_NAME,
            'Key': output_filename
        },
        ExpiresIn=3600
    )

    os.remove(input_path)
    os.remove(output_path)

    return {
        "status": "success",
        "url": url,
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
