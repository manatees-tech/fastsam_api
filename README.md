## fastsam_api

[Original documentation](https://github.com/CASIA-IVA-Lab/FastSAM)

## Development

```
cp .template.env .env
```

```
docker compose up
```

```
curl -X POST "http://localhost:8021/segment" \
     -F "file=@images/dogs.jpg" \
     -F "prompt=a white dog" \
     -F "conf=0.4" \
     -F "iou=0.9"
```
