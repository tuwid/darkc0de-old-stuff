"""
Generate PHP source code using random functions with random arguments.
Use "php" command line program.
"""

VARIABLES = 'abcde'

def setupProject(project):
    DEBUG_PROJECT = True

    php = PhpSource(project)
    # Don't kill any process!
    php.ignore_functions.add('posix_kill')
    # Avoid timeout
    php.ignore_functions.add('ftp_connect')
    php.ignore_functions.add('mysql_connect')
    php.ignore_functions.add('mysql_pconnect')
    php.ignore_functions.add('dns_get_mx')
    php.ignore_functions.add('getmxrr')
    php.ignore_functions.add('dns_check_record')
    php.ignore_functions.add('pfsockopen')
    php.ignore_functions.add('dns_get_record')
    php.ignore_functions.add('gethostbynamel')
    php.ignore_functions.add('ftp_ssl_connect')

    process = PhpProcess(project, ['php', '<source.php>'], timeout=10.0)
    watch = WatchProcess(process, exitcode_score=0.10)
    if watch.cpu:
        watch.cpu.score_weight = 0.3
    stdout = WatchPhpStdout(process, php)
    stdout.max_nb_line = (5000, 1.0)
    del stdout.words['memory']
    del stdout.words['exception']
    stdout.addRegex('Call to undefined function', -1.0)
    if DEBUG_PROJECT:
        stdout.words['warning'] = 0.01
        stdout.words['error'] = 0.01
        stdout.words['fatal'] = 0.10
        stdout.words['assert'] = 0.01
        stdout.words['assertion'] = 0.01
        stdout.ignoreRegex("Only variables can be passed by reference")
        stdout.ignoreRegex("^Fatal error: Can't use function return value in ")
        stdout.ignoreRegex("^Fatal error: Class .* not found")
        stdout.ignoreRegex("^Parse error:")
        stdout.ignoreRegex("sem_get.*Permission denied")
    else:
        stdout.score_weight = 0.3

from fusil.process.create import CreateProcess
from fusil.process.watch import WatchProcess
from fusil.process.stdout import WatchStdout
from fusil.project_agent import ProjectAgent
from fusil.bytes_generator import BytesGenerator
from base64 import b64encode
from random import choice, randint
from weakref import ref
import re

class Base64Generator(BytesGenerator):
    def __init__(self, max_length=10):
        BytesGenerator.__init__(self, 0, max_length)

    def createValue(self):
        value = BytesGenerator.createValue(self)
        return 'base64_decode("%s")' % b64encode(value)

class LengthGenerator(BytesGenerator):
    def __init__(self, max_length=4000):
        BytesGenerator.__init__(self, 0, max_length, bytes_set=set('A'))

    def createValue(self):
        value = BytesGenerator.createValue(self)
        return '"%s"' % value

class WatchPhpStdout(WatchStdout):
    def __init__(self, process, php_source):
        WatchStdout.__init__(self, process)
        self.php_source = ref(php_source)

    def processLine(self, line):
        match = re.search('Call to undefined function ([a-z0-9_]+)', line)
        if match:
            name = match.group(1)
            functions = self.php_source().functions
            if name in functions:
                functions.remove(name)
                self.error("Remove undefined function: %s (new function list length: %s)" % (
                    name, len(functions)))
        else:
            WatchStdout.processLine(self, line)

class NullGenerator:
    def createValue(self):
        return 'null'

class ReferenceGenerator:
    def createValue(self):
        return "&$%s" % choice(VARIABLES)

class VariableGenerator:
    def createValue(self):
        return "$%s" % choice(VARIABLES)

class PhpSource(ProjectAgent):
    def __init__(self, project):
        ProjectAgent.__init__(self, project, "php_source")
        self.generators = [
            Base64Generator(10),
            LengthGenerator(),
            NullGenerator(),
            ReferenceGenerator(),
            VariableGenerator(),
        ]
        self.min_arguments = 0
        self.max_arguments = 10
        self.min_instr = 1
        self.max_instr = 10
        self.ignore_functions = set()
        self.functions = set(PHP_FUNCTIONS)
        self.indent = '   '

    def createArgument(self, func_name, arg_index):
        while True:
            if func_name == 'sleep' and arg_index == 1:
                return '0'

            generator = choice(self.generators)
            value = generator.createValue()
            if func_name == 'isset' and (value == 'null' or value.startswith('&')):
                continue
            return value

    def createFunction(self, name, ):
        if name not in ('print', 'die', 'eval', 'exit', 'isset'):
            nb_argument = randint(self.min_arguments, self.max_arguments)
        else:
            nb_argument = 1

        code = [
            'echo "%s();\\n";' % name,
            'echo "Result: ";',
            'var_dump(',
            self.indent+name+'(',
        ]
        for index in xrange(1, nb_argument+1):
            value = self.createArgument(name, index)
            text = self.indent*2 + '/* %s */ ' % index + value
            if index < nb_argument:
                text += ','
            code.append(text)
        code.append(self.indent+')')
        code.append(');')
        return code

    def createCode(self, functions):
        code = [
            "$a = 42;",
            "$b = Array('hello', 10, 3);",
            "$c = 'Hello World!';",
            "$d = null;",
            "$e = 3.14;",
            '',
        ]
        nb_instr = randint(self.min_instr, self.max_instr)
        for index in xrange(1, nb_instr+1):
            function = choice(functions)
            instr = self.createFunction(function)
            code.append('')
            code.append('echo "--- Instruction %s/%s ---\\n";'
                % (index, nb_instr))
            code.extend(instr)
            code.append('echo "\\n";')
        return code

    def createHeader(self):
        return [
            'echo "error_reporting(E_ALL);\\n\\n";',
            'error_reporting(E_ALL);',
        ]

    def on_session_start(self):
        functions = list(self.functions - self.ignore_functions)
        session_dir = self.project().session.directory
        filename = session_dir.uniqueFilename('source.php')
        header = self.createHeader()
        code = self.createCode(functions)
        code = '\n'.join(['<?php']+header+['']+code+['', '?>'])
        open(filename, 'w').write(code)
        self.send('php_source', filename)

class PhpProcess(CreateProcess):
    def on_php_source(self, filename):
        self.cmdline.arguments[1] = filename
        self.createProcess()

# From "/usr/share/vim/vim71/syntax/php.vim" (vim 7.1)
# From "Function and Methods ripped from php_manual_de.tar.gz Jan 2003"
#
# Skip many PHP extensions
# Skip get_defined_functions, get_defined_vars, get_defined_constants

PHP_FUNCTIONS = """array_change_key_case array_chunk array_combine
array_count_values array_diff_assoc array_diff_uassoc array_diff array_fill
array_filter array_flip array_intersect_assoc array_intersect array_key_exists
array_keys array_map array_merge_recursive array_merge array_multisort
array_pad array_pop array_push array_rand array_reduce array_reverse
array_search array_shift array_slice array_splice array_sum array_udiff_assoc
array_udiff_uassoc array_udiff array_unique array_unshift array_values
array_walk array arsort asort compact count current each end extract in_array
key krsort ksort list natcasesort natsort next pos prev range reset rsort
shuffle sizeof sort uasort uksort usort bcadd bccomp bcdiv bcmod bcmul bcpow
bcpowmod bcscale bcsqrt bcsub bzclose bzcompress bzdecompress bzerrno bzerror
bzerrstr bzflush bzopen bzread bzwrite cal_days_in_month cal_from_jd cal_info
cal_to_jd easter_date easter_days exit frenchtojd gregoriantojd jddayofweek
jdmonthname jdtofrench jdtogregorian jdtojewish jdtojulian jdtounix jewishtojd
juliantojd unixtojd call_user_method_array call_user_method class_exists
get_class_methods get_class_vars get_class get_declared_classes
get_object_vars get_parent_class is_a is_subclass_of method_exists ctype_alnum
ctype_alpha ctype_cntrl ctype_digit ctype_graph ctype_lower ctype_print
ctype_punct ctype_space ctype_upper ctype_xdigit checkdate date getdate
gettimeofday gmdate gmmktime gmstrftime localtime microtime mktime strftime
strtotime time dba_close dba_delete dba_exists dba_fetch dba_firstkey
dba_handlers dba_insert dba_key_split dba_list dba_nextkey dba_open
dba_optimize dba_popen dba_replace dba_sync chdir chroot dir closedir getcwd
opendir readdir rewinddir scandir debug_backtrace debug_print_backtrace
error_log error_reporting restore_error_handler set_error_handler
trigger_error user_error escapeshellarg escapeshellcmd exec passthru
proc_close proc_get_status proc_nice proc_open proc_terminate shell_exec
system basename chgrp chmod chown clearstatcache copy dirname disk_free_space
disk_total_space diskfreespace fclose feof fflush fgetc fgetcsv fgets fgetss
file_exists file_get_contents file_put_contents file fileatime filectime
filegroup fileinode filemtime fileowner fileperms filesize filetype flock
fnmatch fopen fpassthru fputs fread fscanf fseek fstat ftell ftruncate fwrite
glob is_dir is_executable is_file is_link is_readable is_uploaded_file
is_writable is_writeable link linkinfo lstat mkdir move_uploaded_file
parse_ini_file pathinfo pclose popen readfile readlink realpath rename rewind
rmdir set_file_buffer stat symlink tempnam tmpfile touch umask unlink
ftp_alloc ftp_cdup ftp_chdir ftp_chmod ftp_close ftp_connect ftp_delete
ftp_exec ftp_fget ftp_fput ftp_get_option ftp_get ftp_login ftp_mdtm ftp_mkdir
ftp_nb_continue ftp_nb_fget ftp_nb_fput ftp_nb_get ftp_nb_put ftp_nlist
ftp_pasv ftp_put ftp_pwd ftp_quit ftp_raw ftp_rawlist ftp_rename ftp_rmdir
ftp_set_option ftp_site ftp_size ftp_ssl_connect ftp_systype
call_user_func_array call_user_func create_function func_get_arg func_get_args
func_num_args function_exists register_shutdown_function
register_tick_function unregister_tick_function bind_textdomain_codeset
bindtextdomain dcgettext dcngettext dgettext dngettext gettext ngettext
textdomain header headers_list headers_sent setcookie iconv_get_encoding
iconv_mime_decode_headers iconv_mime_decode iconv_mime_encode
iconv_set_encoding iconv_strlen iconv_strpos iconv_strrpos iconv_substr iconv
ob_iconv_handler assert_options assert dl extension_loaded get_cfg_var
get_current_user get_extension_funcs get_include_path
get_included_files get_loaded_extensions get_magic_quotes_gpc
get_magic_quotes_runtime get_required_files getenv getlastmod getmygid
getmyinode getmypid getmyuid getopt getrusage ini_alter ini_get_all ini_get
ini_restore ini_set memory_get_usage php_ini_scanned_files php_logo_guid
php_sapi_name php_uname phpinfo phpversion putenv
restore_include_path set_include_path set_magic_quotes_runtime set_time_limit
version_compare zend_logo_guid zend_version ezmlm_hash mail abs acos acosh
asin asinh atan2 atan atanh base_convert bindec ceil cos cosh decbin dechex
decoct deg2rad exp expm1 floor fmod getrandmax hexdec hypot is_finite
is_infinite is_nan lcg_value log10 log1p log max min mt_getrandmax mt_rand
mt_srand octdec pi pow rad2deg rand round sin sinh sqrt srand tan tanh
mb_convert_case mb_convert_encoding mb_convert_kana mb_convert_variables
mb_decode_mimeheader mb_decode_numericentity mb_detect_encoding
mb_detect_order mb_encode_mimeheader mb_encode_numericentity mb_ereg_match
mb_ereg_replace mb_ereg_search_getpos mb_ereg_search_getregs
mb_ereg_search_init mb_ereg_search_pos mb_ereg_search_regs
mb_ereg_search_setpos mb_ereg_search mb_ereg mb_eregi_replace mb_eregi
mb_get_info mb_http_input mb_http_output mb_internal_encoding mb_language
mb_output_handler mb_parse_str mb_preferred_mime_name mb_regex_encoding
mb_regex_set_options mb_send_mail mb_split mb_strcut mb_strimwidth mb_strlen
mb_strpos mb_strrpos mb_strtolower mb_strtoupper mb_strwidth
mb_substitute_character mb_substr_count mb_substr mime_content_type
mysql_affected_rows mysql_client_encoding mysql_close mysql_connect
mysql_data_seek mysql_db_name mysql_db_query mysql_errno
mysql_error mysql_escape_string mysql_fetch_array mysql_fetch_assoc
mysql_fetch_field mysql_fetch_lengths mysql_fetch_object mysql_fetch_row
mysql_field_flags mysql_field_len mysql_field_name mysql_field_seek
mysql_field_table mysql_field_type mysql_free_result mysql_get_client_info
mysql_get_host_info mysql_get_proto_info mysql_get_server_info mysql_info
mysql_insert_id mysql_list_dbs mysql_list_fields mysql_list_processes
mysql_list_tables mysql_num_fields mysql_num_rows mysql_pconnect mysql_ping
mysql_query mysql_real_escape_string mysql_result mysql_select_db mysql_stat
mysql_tablename mysql_thread_id mysql_unbuffered_query connection_aborted
connection_status constant define defined die eval get_browser
highlight_file highlight_string ignore_user_abort pack show_source sleep
uniqid unpack usleep checkdnsrr closelog define_syslog_variables
dns_check_record dns_get_mx dns_get_record fsockopen gethostbyaddr
gethostbyname gethostbynamel getmxrr getprotobyname getprotobynumber
getservbyname getservbyport ip2long long2ip openlog pfsockopen
socket_get_status socket_set_blocking socket_set_timeout syslog flush ob_clean
ob_end_clean ob_end_flush ob_flush ob_get_clean ob_get_contents ob_get_flush
ob_get_length ob_get_level ob_get_status ob_gzhandler ob_implicit_flush
ob_list_handlers ob_start output_add_rewrite_var output_reset_rewrite_vars
pcntl_exec pcntl_fork pcntl_signal pcntl_waitpid pcntl_wexitstatus
pcntl_wifexited pcntl_wifsignaled pcntl_wifstopped pcntl_wstopsig
pcntl_wtermsig preg_grep preg_match_all preg_match preg_quote
preg_replace_callback preg_replace preg_split posix_ctermid
posix_get_last_error posix_getcwd posix_getegid posix_geteuid posix_getgid
posix_getgrgid posix_getgrnam posix_getgroups posix_getlogin posix_getpgid
posix_getpgrp posix_getpid posix_getppid posix_getpwnam posix_getpwuid
posix_getrlimit posix_getsid posix_getuid posix_isatty posix_kill posix_mkfifo
posix_setegid posix_seteuid posix_setgid posix_setpgid posix_setsid
posix_setuid posix_strerror posix_times posix_ttyname posix_uname ereg_replace
ereg eregi_replace eregi split spliti sql_regcase ftok msg_get_queue
msg_receive msg_remove_queue msg_send msg_set_queue msg_stat_queue sem_acquire
sem_get sem_release sem_remove shm_attach shm_detach shm_get_var shm_put_var
shm_remove_var shm_remove session_cache_expire session_cache_limiter
session_decode session_destroy session_encode session_get_cookie_params
session_id session_is_registered session_module_name session_name
session_regenerate_id session_register session_save_path
session_set_cookie_params session_set_save_handler session_start
session_unregister session_unset session_write_close shmop_close shmop_delete
shmop_open shmop_read shmop_size shmop_write socket_accept socket_bind
socket_clear_error socket_close socket_connect socket_create_listen
socket_create_pair socket_create socket_get_option socket_getpeername
socket_getsockname socket_last_error socket_listen socket_read socket_recv
socket_recvfrom socket_select socket_send socket_sendto socket_set_block
socket_set_nonblock socket_set_option socket_shutdown socket_strerror
socket_write stream_context_create stream_context_get_options
stream_context_set_option stream_context_set_params stream_copy_to_stream
stream_filter_append stream_filter_prepend stream_filter_register
stream_get_contents stream_get_filters stream_get_line stream_get_meta_data
stream_get_transports stream_get_wrappers stream_register_wrapper
stream_select stream_set_blocking stream_set_timeout stream_set_write_buffer
stream_socket_accept stream_socket_client stream_socket_get_name
stream_socket_recvfrom stream_socket_sendto stream_socket_server
stream_wrapper_register addcslashes addslashes bin2hex chop chr chunk_split
convert_cyr_string count_chars crc32 crypt explode fprintf
get_html_translation_table hebrev hebrevc html_entity_decode htmlentities
htmlspecialchars implode join levenshtein localeconv ltrim md5_file md5
metaphone money_format nl_langinfo nl2br number_format ord parse_str print
printf quoted_printable_decode quotemeta rtrim setlocale sha1_file sha1
similar_text soundex sprintf sscanf str_ireplace str_pad str_repeat
str_replace str_rot13 str_shuffle str_split str_word_count strcasecmp strchr
strcmp strcoll strcspn strip_tags stripcslashes stripos stripslashes stristr
strlen strnatcasecmp strnatcmp strncasecmp strncmp strpos strrchr strrev
strripos strrpos strspn strstr strtok strtolower strtoupper strtr
substr_compare substr_count substr_replace substr trim ucfirst ucwords vprintf
vsprintf wordwrap token_get_all token_name base64_decode base64_encode
get_meta_tags http_build_query parse_url rawurldecode rawurlencode urldecode
urlencode doubleval empty floatval get_resource_type gettype
import_request_variables intval is_array is_bool is_callable is_double
is_float is_int is_integer is_long is_null is_numeric is_object is_real
is_resource is_scalar is_string isset print_r serialize settype strval
unserialize unset var_dump var_export wddx_add_vars wddx_deserialize
wddx_packet_end wddx_packet_start wddx_serialize_value wddx_serialize_vars
utf8_decode utf8_encode xml_error_string xml_get_current_byte_index
xml_get_current_column_number xml_get_current_line_number xml_get_error_code
xml_parse_into_struct xml_parse xml_parser_create_ns xml_parser_create
xml_parser_free xml_parser_get_option xml_parser_set_option
xml_set_character_data_handler xml_set_default_handler xml_set_element_handler
xml_set_end_namespace_decl_handler xml_set_external_entity_ref_handler
xml_set_notation_decl_handler xml_set_object
xml_set_processing_instruction_handler xml_set_start_namespace_decl_handler
xml_set_unparsed_entity_decl_handler xmlrpc_decode_request xmlrpc_decode
xmlrpc_encode_request xmlrpc_encode xmlrpc_get_type
xmlrpc_parse_method_descriptions xmlrpc_server_add_introspection_data
xmlrpc_server_call_method xmlrpc_server_create xmlrpc_server_destroy
xmlrpc_server_register_introspection_callback xmlrpc_server_register_method
xmlrpc_set_type zip_close zip_entry_close zip_entry_compressedsize
zip_entry_compressionmethod zip_entry_filesize zip_entry_name zip_entry_open
zip_entry_read zip_open zip_read gzclose gzcompress gzdeflate gzencode gzeof
gzfile gzgetc gzgets gzgetss gzinflate gzopen gzpassthru gzputs gzread
gzrewind gzseek gztell gzuncompress gzwrite readgzfile
zlib_get_coding_type""".split()

