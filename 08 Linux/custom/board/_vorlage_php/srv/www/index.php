<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>Hallo, PHP!</title>
        <style>
            html, body {
                font-size: 12pt;
                font-family: sans-serif;
                margin: 0;

                height: 100%;
                min-height: 100%;
            }

            html {
                background-image: url(bg.svg);
                background-size: cover;
                background-repeat: no-repeat;
            }
        </style>
    </head>
    <body>
        <? if ($_SERVER["REQUEST_METHOD"] == "GET") { ?>
            <h1>Hallo, PHP!</h1>

            <form method="post">
                Wie heißt du? <input name="mein_name" />
                <br/>
                <input type="submit">
            </form>
        <? } else {
            $meinName = $_POST["mein_name"];
            if (empty($meinName)) $meinName = "Fremder"; ?>

            <h1>Hallo, <?= $meinName ?></h1>
        <? } ?>
    </body>
</html>
