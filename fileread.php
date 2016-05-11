<html>
<body>

<?PHP
$File = "keyloggeroutput.txt";


 if (isset($File))
 {
   $Handle = @fopen ($File, "r"); // '@' suppresses external errors

   if ($Handle)
   {
     $FileText = fread ($Handle, 10000); // Read up to 10,000 Bytes

     fclose ($Handle);

     // Fix HTML tags that may be there

     $SafeText1  = str_replace ("Space", " ", $FileText);
$SafeText2  = str_replace ("Return", "\n", $SafeText1);
$SafeText3  = str_replace ("Oem_Comma", ",", $SafeText2);
$SafeText  = str_replace ("Oem_Period", ".", $SafeText3);

     // Now it is safe to display it

     echo " <H2 ALIGN=CENTER>File: $File</H2>\n";

     echo "<PRE>\n";
     echo $SafeText;
     echo "</PRE>\n";
   }
   else
   {
     echo " <H3>Error: File '$File' is not accessible.</H3>\n";
   }
 }
?>
</body>
</html>
