import os

def phc_commandline():
    #os.system("phc -b input output")
    os.system("phc -p input output")

def phc_homotopy(start_system):
    from phcpy.phcpy2c3 import py2c_set_seed
    from phcpy.trackers import track
    py2c_set_seed(2019)
    #p = ['x^2 + y - 3;', 'x + 0.125*y^2 - 1.5;']
    #p = ['x^2 + y^2 - 3;','x^2 + y^2 - 10;']
    p = start_system
    print('constructing a total degree start system ...')
    from phcpy.solver import total_degree_start_system as tds
    q, qsols = tds(p)
    print('q:', q)
    from phcpy.trackers import initialize_standard_tracker
    from phcpy.trackers import initialize_standard_solution
    from phcpy.trackers import next_standard_solution, next_quaddobl_solution
    initialize_standard_tracker(p, q, False) # True)
    # initialize_standard_tracker(p, q, True)
    from phcpy.solutions import strsol2dict
    import matplotlib.pyplot as plt
    plt.ion()
    fig = plt.figure()
    for k in range(len(qsols)):
        if(k == 0):
            axs = fig.add_subplot(221)
        elif(k == 1):
            axs = fig.add_subplot(222)
        elif(k == 2):
            axs = fig.add_subplot(223)
        elif(k == 3):
            axs = fig.add_subplot(224)
        startsol = qsols[k]
        initialize_standard_solution(len(p),startsol)
        dictsol = strsol2dict(startsol)
        xpoints =  [dictsol['x']]
        ypoints =  [dictsol['y']]
        for k in range(300):
            ns = next_standard_solution()
            #print("next standard solution:",ns)
            #ns = next_quaddobl_solution()
            dictsol = strsol2dict(ns)
            xpoints.append(dictsol['x'])
            ypoints.append(dictsol['y'])
            tval = dictsol['t'].real
            #print("tvalue:",tval)
            # tval = eval(dictsol['t'].lstrip().split(' ')[0])
            if(tval == 1.0):
                break
        print(ns)
        xre = [point.real for point in xpoints]
        yre = [point.real for point in ypoints]
        axs.set_xlim(min(xre)-0.3, max(xre)+0.3)
        axs.set_ylim(min(yre)-0.3, max(yre)+0.3)
        dots, = axs.plot(xre,yre,'r-')
        fig.canvas.draw()
    fig.canvas.draw()
    ans = input('hit return to exit')

if __name__=="__main__":
    #phc_commandline()
    phc_homotopy(['x^4 + y^4 - 3;','x-1;'])
