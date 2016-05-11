#!usr/bin/perl

##
# Coded By KuNdUz
##

use Tk;
use HTTP::Request;
use LWP::UserAgent;

$mw = MainWindow->new( -background => "black", -cursor=>"crosshair");
$mw->geometry("1070x325+100+300");
$mw->title("|_^_| Admin Control Panel Finder v1.2 |_^_|");
$mw->resizable(0,0);

$statusbar = "|_^_| Admin Control Panel Finder v1.2 |_^_|";
$statusbottom = $mw->Label(-textvariable => \$statusbar, -relief => 'flat', -background => "black", -foreground => "red", -font => "Verdana 7", -width => 120)->place(-x => 240, -y => 307);
$mw->Label(-background => "black", -foreground => "black")->pack();
$stat = "Control Panel Found";
$sta = $mw->Label(-textvariable => \$stat, -relief => 'flat', -background => "black", -foreground => "red", -font => "Verdana 9")->place(-x => 380, -y => 10);
$stat1 = "Control Panel Not Found";
$st = $mw->Label(-textvariable => \$stat1, -relief => 'flat', -background => "black", -foreground => "red", -font => "Verdana 9")->place(-x => 786, -y => 10);
$test1 = $mw->Scrolled("Text", -scrollbars => 'oe', -font => "Verdana 8", -background => "black", -foreground => "red", -selectbackground => "red", -insertbackground => "red", -relief => "ridge", -width => 55, -height=> 20)->pack(-side => 'right', -anchor => 'e');
$test2 = $mw->Scrolled("Text", -scrollbars => 'oe', -font => "Verdana 8", -background => "black", -foreground => "red", -selectbackground => "red", -insertbackground => "red", -relief => "ridge", -width => 55, -height=> 20)->pack(-side => 'right', -anchor => 'e');
$mw->Label(-background => "black", -foreground => "black")->pack();
$mw->Label(-background => "black", -foreground => "black")->pack();
$mw->Label(-background => "black", -foreground => "black")->pack();
$mw->Label(-background => "black", -foreground => "red", -font => "Verdana 9", -text => "                    Enter Site ")->pack(-anchor => 'nw');
$mw->Entry(-background => "black", -foreground => "red", -selectbackground => "black", -insertbackground => "red", -width => 40, -relief => "ridge", -textvariable => \$site)->pack(-anchor => 'nw');
$mw->Label(-background => "black", -foreground => "red", -font => "Verdana 9", -text => "          Enter Site Source Code ")->pack(-anchor => 'nw');
$mw->Entry(-background => "black", -foreground => "red", -selectbackground => "black", -insertbackground => "red", -width => 40, -relief => "ridge", -textvariable => \$code)->pack(-anchor => 'nw');
$mw->Label(-background => "black", -foreground => "black")->pack();
$mw->Label(-background => "black", -foreground => "black")->pack();
$mw->Button(-activebackground => "red",  -activeforeground => "black",  -background => "black", -foreground => "red", -font => "Verdana 7", -relief => "groove", -text => "Start", -width => 5, -command => \&scan)->place(-x => 40, -y => 190);
$mw->Button(-activebackground => "red",  -activeforeground => "black",  -background => "black", -foreground => "red", -font => "Verdana 7", -relief => "groove", -text => "Stop", -width => 5, -command => \&sto )->place(-x => 95, -y => 190);
$mw->Button(-activebackground => "red",  -activeforeground => "black",  -background => "black", -foreground => "red", -font => "Verdana 7", -relief => "groove", -text => "Clear",  -width => 5, -command => \&cle)->place(-x => 150, -y => 190);
$mw->Button(-activebackground => "red",  -activeforeground => "black",  -background => "black", -foreground => "red", -font => "Verdana 7", -relief => "groove", -text => "Help/About", -width => 9, -command => \&heaab)->place(-x => 50, -y => 240);
$mw->Button(-activebackground => "red",  -activeforeground => "black",  -background => "black", -foreground => "red", -font => "Verdana 7", -relief => "groove", -text => "Exit",  -width => 5, -command => sub { exit })->place(-x => 133, -y => 240);

MainLoop;

sub heaab {
$about = $mw->Toplevel(-background => "black", -cursor=>"crosshair");
$about->geometry("500x422+425+250");
$about->title("|_^_| Admin Control Panel Finder v1.2 |_^_|");
$about->resizable(0,0);
$about->Label(-background => "black", -foreground=>"red")->pack();
$about->Label(-background => "black", -foreground=>"red", -font=> "Cambria 10", -text => "|_^_| Admin Control Panel Finder v1.2 Help |_^_|\n")->pack();
$about->Label(-background => "black", -foreground=>"red", -font=> "Cambria 10",  -text => " -Enter Site-\nEnter Target address,\n exemplarily www.site.com or www.site.com/path")->pack();
$about->Label(-background => "black", -foreground=>"red", -font=> "Cambria 10",  -text => " -Enter Site Source Code-\nEnter target site source code.\n Site source code php is the write php or\n Site source code asp is the write asp")->pack();
$about->Label(-background => "black", -foreground=>"red", -font=> "Cambria 10",  -text => "\nEx:\n Enter Site : www.target.com\n Enter Site Source Code : php")->pack();
$about->Label(-background => "black", -foreground=>"red")->pack();
$about->Label(-background => "black", -foreground=>"red", -font=> "Cambria 10", -text => "|_^_| Admin Control Panel Finder v1.2 About |_^_|\n")->pack();
$about->Label(-background => "black",-foreground => "red",-font => "wingdings 22", -text => "7")->pack();
$about->Label(-background => "black", -foreground=>"red", -font=> "Cambria 11",  -text => "Coded By KuNdUz")->pack();
$about->Label(-background => "black", -foreground=>"red", -font=> "Cambria 11",  -text => "Enjoy! :)")->pack();
$about->Label(-background => "black", -foreground => "red", -font => "Cambria 8",  -text => "10/12/2008")->pack(-anchor => "se");
$about->Button(-activebackground => "red",  -activeforeground => "black",  -background => "black", -foreground => "red", -relief => "groove", -font=> "Verdana 7", -text => "Exit", -command => [$about => 'destroy'])->pack(-fill => "both");
}

sub cle {
$test1->delete("0.0", "end");
$test2->delete("0.0", "end");
}

sub sto {
$sisite = "",
$ways = "",
@path1 = ""
}

sub scan {

$test1->delete("0.0", "end");
$test2->delete("0.0", "end");

$sisite = $site;

if ( $sisite !~ /^http:/ ) {
$sisite = 'http://' . $sisite;
}
if ( $sisite !~ /\/$/ ) {
$sisite = $sisite . '/';
}

if($code eq "php"){
@path1=('admin/','administrator/','moderator/','webadmin/','adminarea/','bb-admin/','adminLogin/','admin_area/','panel-administracion/','instadmin/',
'memberadmin/','administratorlogin/','adm/','admin/account.php','admin/index.php','admin/login.php','admin/admin.php','admin/account.php',
'admin_area/admin.php','admin_area/login.php','siteadmin/login.php','siteadmin/index.php','siteadmin/login.html','admin/account.html','admin/index.html','admin/login.html','admin/admin.html',
'admin_area/index.php','bb-admin/index.php','bb-admin/login.php','bb-admin/admin.php','admin/home.php','admin_area/login.html','admin_area/index.html',
'admin/controlpanel.php','admin.php','admincp/index.asp','admincp/login.asp','admincp/index.html','admin/account.html','adminpanel.html','webadmin.html',
'webadmin/index.html','webadmin/admin.html','webadmin/login.html','admin/admin_login.html','admin_login.html','panel-administracion/login.html',
'admin/cp.php','cp.php','administrator/index.php','administrator/login.php','nsw/admin/login.php','webadmin/login.php','admin/admin_login.php','admin_login.php',
'administrator/account.php','administrator.php','admin_area/admin.html','pages/admin/admin-login.php','admin/admin-login.php','admin-login.php',
'bb-admin/index.html','bb-admin/login.html','bb-admin/admin.html','admin/home.html','login.php','modelsearch/login.php','moderator.php','moderator/login.php',
'moderator/admin.php','account.php','pages/admin/admin-login.html','admin/admin-login.html','admin-login.html','controlpanel.php','admincontrol.php',
'admin/adminLogin.html','adminLogin.html','admin/adminLogin.html','home.html','rcjakar/admin/login.php','adminarea/index.html','adminarea/admin.html',
'webadmin.php','webadmin/index.php','webadmin/admin.php','admin/controlpanel.html','admin.html','admin/cp.html','cp.html','adminpanel.php','moderator.html',
'administrator/index.html','administrator/login.html','user.html','administrator/account.html','administrator.html','login.html','modelsearch/login.html',
'moderator/login.html','adminarea/login.html','panel-administracion/index.html','panel-administracion/admin.html','modelsearch/index.html','modelsearch/admin.html',
'admincontrol/login.html','adm/index.html','adm.html','moderator/admin.html','user.php','account.html','controlpanel.html','admincontrol.html',
'panel-administracion/login.php','wp-login.php','adminLogin.php','admin/adminLogin.php','home.php','admin.php','adminarea/index.php',
'adminarea/admin.php','adminarea/login.php','panel-administracion/index.php','panel-administracion/admin.php','modelsearch/index.php',
'modelsearch/admin.php','admincontrol/login.php','adm/admloginuser.php','admloginuser.php','admin2.php','admin2/login.php','admin2/index.php',
'adm/index.php','adm.php','affiliate.php','adm_auth.php','memberadmin.php','administratorlogin.php'
);

foreach $ways(@path1){
$statusbar = "Scaning path: " . $ways;
$statusbottom->update();
$statusbar = "|_^_| Admin Control Panel Finder v1.2 |_^_|";
$final=$sisite.$ways;
$req=HTTP::Request->new(GET=>$final);
$ua=LWP::UserAgent->new();
$ua->timeout(30);
$response=$ua->request($req);

if($response->content =~ /Username/ ||
$response->content =~ /Password/ ||
$response->content =~ /username/ ||
$response->content =~ /password/ ||
$response->content =~ /USERNAME/ ||
$response->content =~ /PASSWORD/ ||
$response->content =~ /Senha/ ||
$response->content =~ /senha/ ||
$response->content =~ /Personal/ ||
$response->content =~ /Usuario/ ||
$response->content =~ /Clave/ ||
$response->content =~ /Usager/ ||
$response->content =~ /usager/ ||
$response->content =~ /Sing/ ||
$response->content =~ /passe/ ||
$response->content =~ /P\/W/ || 
$response->content =~ /Admin Password/
){
$test2->insert('end', $final."\n");
}else{
$test1->insert('end', $final."\n");
}
}
}

if($code eq "asp"){
@path1=('admin/','administrator/','moderator/','webadmin/','adminarea/','bb-admin/','adminLogin/','admin_area/','panel-administracion/','instadmin/',
'memberadmin/','administratorlogin/','adm/','account.asp','admin/account.asp','admin/index.asp','admin/login.asp','admin/admin.asp',
'admin_area/admin.asp','admin_area/login.asp','admin/account.html','admin/index.html','admin/login.html','admin/admin.html',
'admin_area/admin.html','admin_area/login.html','admin_area/index.html','admin_area/index.asp','bb-admin/index.asp','bb-admin/login.asp','bb-admin/admin.asp',
'bb-admin/index.html','bb-admin/login.html','bb-admin/admin.html','admin/home.html','admin/controlpanel.html','admin.html','admin/cp.html','cp.html',
'administrator/index.html','administrator/login.html','administrator/account.html','administrator.html','login.html','modelsearch/login.html','moderator.html',
'moderator/login.html','moderator/admin.html','account.html','controlpanel.html','admincontrol.html','admin_login.html','panel-administracion/login.html',
'admin/home.asp','admin/controlpanel.asp','admin.asp','pages/admin/admin-login.asp','admin/admin-login.asp','admin-login.asp','admin/cp.asp','cp.asp',
'administrator/account.asp','administrator.asp','login.asp','modelsearch/login.asp','moderator.asp','moderator/login.asp','administrator/login.asp',
'moderator/admin.asp','controlpanel.asp','admin/account.html','adminpanel.html','webadmin.html','pages/admin/admin-login.html','admin/admin-login.html',
'webadmin/index.html','webadmin/admin.html','webadmin/login.html','user.asp','user.html','admincp/index.asp','admincp/login.asp','admincp/index.html',
'admin/adminLogin.html','adminLogin.html','admin/adminLogin.html','home.html','adminarea/index.html','adminarea/admin.html','adminarea/login.html',
'panel-administracion/index.html','panel-administracion/admin.html','modelsearch/index.html','modelsearch/admin.html','admin/admin_login.html',
'admincontrol/login.html','adm/index.html','adm.html','admincontrol.asp','admin/account.asp','adminpanel.asp','webadmin.asp','webadmin/index.asp',
'webadmin/admin.asp','webadmin/login.asp','admin/admin_login.asp','admin_login.asp','panel-administracion/login.asp','adminLogin.asp',
'admin/adminLogin.asp','home.asp','admin.asp','adminarea/index.asp','adminarea/admin.asp','adminarea/login.asp','admin-login.html',
'panel-administracion/index.asp','panel-administracion/admin.asp','modelsearch/index.asp','modelsearch/admin.asp','administrator/index.asp',
'admincontrol/login.asp','adm/admloginuser.asp','admloginuser.asp','admin2.asp','admin2/login.asp','admin2/index.asp','adm/index.asp',
'adm.asp','affiliate.asp','adm_auth.asp','memberadmin.asp','administratorlogin.asp','siteadmin/login.asp','siteadmin/index.asp','siteadmin/login.html'
);

foreach $ways(@path1){
$statusbar = "Scaning path: " . $ways;
$statusbottom->update();
$statusbar = "|_^_| Admin Control Panel Finder v1.2 |_^_|";
$final=$sisite.$ways;
$req=HTTP::Request->new(GET=>$final);
$ua=LWP::UserAgent->new();
$ua->timeout(30);
$response=$ua->request($req);

if($response->content =~ /Username/ ||
$response->content =~ /Password/ ||
$response->content =~ /username/ ||
$response->content =~ /password/ ||
$response->content =~ /USERNAME/ ||
$response->content =~ /PASSWORD/ ||
$response->content =~ /Senha/ ||
$response->content =~ /senha/ ||
$response->content =~ /Personal/ ||
$response->content =~ /Usuario/ ||
$response->content =~ /Clave/ ||
$response->content =~ /Usager/ ||
$response->content =~ /usager/ ||
$response->content =~ /Sing/ ||
$response->content =~ /passe/ ||
$response->content =~ /P\/W/ || 
$response->content =~ /Admin Password/
){
$test2->insert('end', $final."\n");
}else{
$test1->insert('end', $final."\n");
}
}
}
}

##
# Coded By KuNdUz
##
