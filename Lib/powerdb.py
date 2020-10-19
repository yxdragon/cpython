from pdb import Pdb
 
class Powerdb(Pdb):
    '''Powerdb is a nondestructive debug tool. (when we use pdb, we need add pdb.set_trace() to the source code, and remove them after debug)
Usage:
    from powerdb import debug
    debug(__file__) # just delete or # this line after debug

    your code ......
    need not insert any code, but the note "#bp" after or upon one line.
    such as:

    s = 0
    for i in range(10):
        s += i #bp

    or:
    
    s = 0
    for i in range(10):
        #bp
        s += i

When in breakpoint:
    :r  debug -return
    :s  debug -step
    :n  debug -next
    :c  debug -continue
    :q  debug -quit
    :w  debug -where
    :m  refresh the #bp mark
    (you can modify and save the code, and refresh the mark)

    other input would be treat as script
    '''
    def onecmd(self, line):
        if line==':r':
            return self.do_return(None)
        if line==':s':
            return self.do_step(None)
        if line==':n':
            return self.do_next(None)
        if line==':c':
            return self.do_continue(None)
        if line==':u':
            return self.do_up(None)
        if line==':d':
            return self.do_down(None)
        if line==':l':
            return self.do_list(None)
        if line==':w':
            return self.do_where(None)
        if line==':q':
            return self.do_quit(None)
        if line==':m':
            return self.refresh_bpmark(None)
        self.default(line)
    
    def interaction(self, frame, traceback):
        if self.first and not self.break_here(frame):
            self.do_continue(None)
        else: super().interaction(frame, traceback)
        self.first = False

    def dispatch_call(self, frame, arg):
        filename = self.canonic(frame.f_code.co_filename)
        if filename[0] != '<' and filename not in self.breaks:
            self.breaks[filename] = []
            marks = self.collect_bpmark(filename)
            for i in marks:
                self.set_break(filename, i)
        return super().dispatch_call(frame, arg)

    def refresh_bpmark(self, name=None, mk='#bp'):
        fs = self.breaks.keys()
        self.clear_all_breaks()
        for i in fs:
            marks = self.collect_bpmark(i)
            for j in marks:
                self.set_break(i, j)
        self.message('break point mark refreshed!')
    
    def collect_bpmark(self, name, mk='#bp'):
        with open(name, encoding='utf-8') as f:
            lines = f.read().split('\n')
        ls = [i.strip().replace(' ','') for i in lines]
        no = [i for i,j in enumerate(ls) if j.endswith(mk)]
        return [i + 1 + ls[i].startswith(mk) for i in no]

    def run(self, cmd, globals=None, locals=None):
        cmd = cmd.replace('debug(__file__)', '# debug(__file__)')
        super().run(cmd, globals, locals)
        
    def debug(self, *arg, **key):
        self.first = True
        Pdb._runscript(self, *arg, **key)

def debug(path):
    Powerdb().debug(path)
    import sys
    sys.exit()

if __name__ == '__main__':
    pass

