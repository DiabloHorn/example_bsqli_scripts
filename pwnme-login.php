<?php
/*
    DiabloHorn https://diablohorn.wordpress.com
*/
$username = "root";
$password = "root";

$link = mysql_connect('localhost',$username,$password);

if(!$link){
    die(mysql_error());
}

if(!mysql_select_db("mysql",$link)){
    die(mysql_error());
}

session_start();

if($_SERVER["REQUEST_METHOD"] == "POST"){
    if($_POST['user'] === "webuser" && $_POST['pass'] === "webpass"){        
        $_SESSION['login'] = "ok";
        echo "login OK";
    }
}
if($_SESSION['login'] === "ok"){
    $result = mysql_query("select user,host from user where user='" . $_GET['name'] . "'",$link);

    echo "<html><body>";
    if(mysql_num_rows($result) > 0){
        echo "User exists<br/>";
    }else{
        echo "User does not exist<br/>";
    }

    if($_GET['debug'] === "1"){    
        while ($row = mysql_fetch_assoc($result)){
            echo $row['user'] . ":" . $row['host'] . "<br/>";
        }
    }
    echo "</html></body>";
    mysql_free_result($result);
}else{
    echo "please login first";
}

mysql_close($link);
?>
