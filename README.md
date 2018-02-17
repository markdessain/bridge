# bridge

```
docker build -t bridge .
docker run -v $(docker_path):/home/project -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix$DISPLAY -it bridge
```

```
python3 card_recognition/main.py
