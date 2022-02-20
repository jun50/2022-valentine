<!DOCTYPE html>
<html lang="ja">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>認証</title>
</head>

<body>
    <div style="text-align: center;">
        <?php
        if ($_POST) {
            $dsn = 'mysql:dbname=vale;host=194.135.92.179';
            $user = 'vale';
            $password = 'NekomimiMaid!';

            try {
                $dbh = new PDO($dsn, $user, $password);
            } catch (PDOException $e) {
                echo "<p style='color: red;font-size: 1.2rem;'>データベースエラーです。</p>";
                exit;
            }

            $sql = 'SELECT * FROM user WHERE user=:user';
            $prepare = $dbh->prepare($sql);
            $prepare->bindValue(':user', $_POST["user"], PDO::PARAM_STR);
            $prepare->execute();
            $result = $prepare->fetchAll(PDO::FETCH_ASSOC);

            if ($result[0]['pw'] === md5($_POST["password"])) {
                require("congratulations.php");
                congratulations();
                exit;
            } else {
                echo "<p style='color: red;font-size: 1.2rem;'>データベース上のパスワードと合致しませんでした。</p>";
            }
        }
        ?>
            <form method="post">
                <h1>パスワードを入力して認証してください。</h1>
                ユーザー名　<input type="text" placeholder="your name?" name="user"><br>
                パスワード　<input type="password" placeholder="Password" name="password"><br>
                <button style="margin-top: 12px;">Login</button>
            </form>
    </div>
</body>

</html>
