%module Pcap

/********************************************************************/
/* libpcap to Python interface file for SWIG                        */
/*                                                                  */
/* written by Aaron L. Rhodes, 11 Nov 98                            */
/*                                                                  */
/* -- Added BPF filtering support (rudimentary)                     */
/*    22 Feb 99                                                     */
/********************************************************************/

//
// Headers needed in the generated .c file.  Note: these may change
// depending on where and how you have installed the pcap library
//
%{
#include <pcap/pcap.h>
#include <net/bpf.h>
%}


/**************************************************/
/* These are helper functions that take the place */
/* of a few libpcap functions.                    */
/* These functions will have wrappers generated   */
/* for them by SWIG                               */
/**************************************************/

%{

/* 
 * This function matches the prototype of a libpcap callback function. 
 * It is passed as the function callback for libpcap.
 * However, the *PyFunc pointer actually refers to a Python callable object. 
 * This function executes the python function, translating the input
 * arguments to Python and passing them to the script function as necessary.
 */

void PythonCallBack(u_char *PyFunc,
                    const struct pcap_pkthdr *header,
                    const u_char *packetdata)
{
   PyObject *func, *arglist;
   unsigned int *len;
   len    = (unsigned int *)&header->len;
   func = (PyObject *) PyFunc;
   arglist = Py_BuildValue("is#",*len,packetdata,*len);
   PyEval_CallObject(func,arglist);
   Py_DECREF(arglist);
}

/* Wraps pcap_loop so that a Python function can be used as a callback */
void py_loop(pcap_t *p, int cnt, PyObject *PyFunc) {
  pcap_loop(p,cnt,PythonCallBack,(u_char *) PyFunc);
  Py_INCREF(PyFunc);
}

/* Wrapper for pcap_dispatch */
void py_dispatch(pcap_t *p, int cnt, PyObject *PyFunc) {
  pcap_dispatch(p,cnt,PythonCallBack,(u_char *) PyFunc);
  Py_INCREF(PyFunc);
}

/* Helper functions for passing correct args to pcap_compile */
struct bpf_program *new_bpf_program(void) {
  struct bpf_program *bprog = (struct bpf_program*) malloc(sizeof(struct bpf_program));
  return bprog;
}

void delete_bpf_program(struct bpf_program *bprog) {
  free(bprog);   
}

%}
///////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////

// -------------------------------------------------------------------
// SWIG typemap allowing us to grab a Python callable object
// -------------------------------------------------------------------
%typemap(python,in) PyObject *PyFunc {
  if (!PyCallable_Check($source)) {
      PyErr_SetString(PyExc_TypeError, "Need a callable object!");
      return NULL;
  }
  $target = $source;
}

// -------------------------------------------------------------------
// EXCEPTION handling
// -------------------------------------------------------------------
%except {
    $function
}

// -------------------------------------------------------------------
// Function declarations for other functions from libpcap that
// need wrapping by SWIG
// -------------------------------------------------------------------

%name(loop)          void py_loop(pcap_t *p, int cnt, PyObject *PyFunc) ;
%name(dispatch)      void py_dispatch(pcap_t *p, int cnt, PyObject *PyFunc) ;
%name(lookupdev)     char *pcap_lookupdev(char *);
%name(lookupnet)     int pcap_lookupnet(char *, bpf_u_int32 *, bpf_u_int32 *, char *);
%name(open_live)     pcap_t *pcap_open_live(char *, int, int, int, char *);
%name(open_offline)  pcap_t *pcap_open_offline(const char *, char *);
%name(close)         void pcap_close(pcap_t *);
%name(next)          const u_char* pcap_next(pcap_t *, struct pcap_pkthdr *);
%name(stats)         int pcap_stats(pcap_t *, struct pcap_stat *);
%name(setfilter)     int pcap_setfilter(pcap_t *, struct bpf_program *);
%name(perror)        void pcap_perror(pcap_t *, char *);
%name(strerror)      char *pcap_strerror(int);
%name(geterr)        char *pcap_geterr(pcap_t *);
%name(compile)       int pcap_compile(pcap_t *, struct bpf_program *fp, char *str,
                                         int optimize, int netmask);
%name(datalink)      int pcap_datalink(pcap_t *);
%name(snapshot)      int pcap_snapshot(pcap_t *);
%name(is_swapped)    int pcap_is_swapped(pcap_t *);
%name(major_version) int pcap_major_version(pcap_t *);
%name(minor_version) int pcap_minor_version(pcap_t *);
%name(file)          FILE *pcap_file(pcap_t *);
%name(fileno)        int pcap_fileno(pcap_t *);
%name(dump_open)     pcap_dumper_t *pcap_dump_open(pcap_t *, const char *);
%name(dump_close)    void pcap_dump_close(pcap_dumper_t *);
%name(dump)          void pcap_dump(u_char *, const struct pcap_pkthdr *, const u_char *);
%name(bpfprog_new)   struct bpf_program *new_bpf_program(void);
%name(bpfprog_del)   void delete_bpf_program(struct bpf_program *bprog);

