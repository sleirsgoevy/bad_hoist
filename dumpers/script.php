<?php 


$file_name = 'baseAddress.txt'; 
if ($_POST['value'] == "startfile"){  
	unlink($file_name);
}
else{
	$fp = fopen($file_name, 'a');
	fwrite($fp, $_POST['value'].PHP_EOL);  
	fclose($fp); 
}
?>  
