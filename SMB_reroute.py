#!/usr/bin/env python
# cliechti@gmx.net
# python license

import select, socket, sys, threading

class Observer:
    """base class for views in the Observer Pattern"""
    def update(self, subject, *args, **kwargs):
        """Implement this method in a concrete observer."""
        raise "not implemented"

class Subject:
    """base class for a model in the Observer Pattern."""
    def __init__(self):
        """don't forget to call this in derrived classes.
        it initalizes the list of observers"""
        self.observerList = []
    def attach(self, observer):
        """attach an observer to this model."""
        self.observerList.append(observer)
    def detach(self, observer):
        """detach an observer from this model."""
        self.observerList.remove(observer)
    def notify(self, *args, **kwargs):
        """for use by the model. this method is called to notify
        observers about changes in the model."""
        for observer in self.observerList:
            observer.update(self, *args, **kwargs)

class DirectForwarder(Subject, threading.Thread):
    def __init__(self, localhp, targethp):
        Subject.__init__(self)
        threading.Thread.__init__(self)
        self.localhp  = localhp
        self.targethp = targethp
        self.verbose = 0
        self.active = 1
        self.setName('%d->%s:%d' % (localhp[1], targethp[0], targethp[1]))
        self.setDaemon(1)

    def run(self, forever = 1):
        sserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sserver.bind(self.localhp)
        sserver.listen(1)
        while forever and self.active:
            self.notify('listening on %s:%d' % self.localhp)
            while self.active:
                ready, _, _= select.select([sserver],[],[sserver], 3) # with timeout
                if ready: break
            else:
                self.notify('deactivated')
                break
            self.slocal, addr = sserver.accept()
            self.notify('Connected by %s:%d' % addr)

            #connecting to target
            self.notify('Connecting to %s:%d' % self.targethp)
            self.starget = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.starget.connect(self.targethp)
            self.notify('Connection open')

            self.slocal.setblocking(0)
            self.starget.setblocking(0)
            try:
                alive = 1
                while alive:
                    ready_to_read, ready_to_write, in_error = \
                        select.select(
                          [self.slocal, self.starget],  #potential_readers
                          [],                           #potential_writers
                          [self.slocal, self.starget],  #potential_errs
                          3)                            #timeout
                    for s in ready_to_read:
                        if s is self.slocal:
                            r = self.slocal.recv(8192)
                            if r:
                                self.starget.send(r)
                                if self.verbose: self.notify('->t %d' % len(r))
                            else:
                                alive = 0
                        elif s is self.starget:
                            r = self.starget.recv(8192)
                            if r:
                                self.slocal.send(r)
                                if self.verbose: self.notify('<-t %d' % len(r))
                            else:
                                alive = 0
                    if in_error: alive = 0
            except socket.error, msg:
                print msg

            self.notify("closing connections...")
            #switch off blocking to force threads to exit
            #t.setblocking(0);
            #conn.setblocking(0);

            self.slocal.close()
            self.starget.close()
        self.notify("Shutdown...")
        self.active = 0
        
    def stop(self):
        if self.active:
            self.active = 0
            self.join()

    def stat(self):
        return ('STOPPED','SERVICE')[self.active!=0]

if __name__ == '__main__':
    import os
    if len(sys.argv) != 3:
        print "USAGE: %s username host " % sys.argv[0]
        sys.exit(1);
    username, host = sys.argv[1:3]

    class MSG(Observer):
        def update(self, model, arg):
            print arg
    f = DirectForwarder(('127.0.0.2', 139), ('127.0.0.1', 1390))
    f.attach(MSG())
    f.start()
    os.system('ssh -c blowfish -L 1390:%s:139 %s@%s' % (host, username, host))
    f.stop()
