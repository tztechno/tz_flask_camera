<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Camera Capture</title>
</head>

<body>
    <h1>Camera Capture</h1>
    <div>
        <img id="videoFeed" src="{{ url_for('video_feed') }}" alt="Video Feed" width="640" height="480">
    </div>
    <form action="/capture" method="POST">
        <button type="submit">Capture</button>
    </form>
    <br>
    <button id="toggleButton" onclick="toggleCamera()">Turn Camera Off</button>

    <script>
        let cameraOn = true;  // 初期状態ではカメラがオン

        function toggleCamera() {
            const action = cameraOn ? 'off' : 'on';  // カメラの現在の状態に基づいてアクションを設定

            fetch('/toggle_camera', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `action=${action}`
            })
                .then(response => response.text())
                .then(() => {
                    cameraOn = !cameraOn;  // 状態を反転
                    const button = document.getElementById('toggleButton');
                    button.textContent = cameraOn ? 'Turn Camera Off' : 'Turn Camera On';  // ボタンのテキストを更新
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
    </script>
</body>

</html>
