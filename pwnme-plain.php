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
mysql_close($link);
?>
