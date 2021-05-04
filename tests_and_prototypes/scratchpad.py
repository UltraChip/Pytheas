## Python Scratch Pad

def acap(poll_interval, cap_interval, poll_period, bk_interval):
    # Performs automatic capture of sensor data & pictures
    filename = "{}_ACAP_{}.csv".format(sessionName, strftime("%Y%m%d-%H%M%S"))
    subheader("Automatic Data Capture")
    acapThreads = []
    with open("{}/{}".format(sessionPath, filename), mode='w') as file:
        dx = csv.writer(file)
        dx.writerow(["T", "LTime", "Pressure", "Depth", "ETemp", "ITemp"])
        logging.info("Automatic data capture under file name " + filename + " has begun.")

    for tick in range(1, poll_period + 1):
        startTime = time()
        with open("{}/{}".format(sessionPath, filename), mode='w') as file:
            ltime, pressure, depth, etemp, itemp = getReadings()
            dx.writerow([tick, ltime, pressure, depth, etemp, itemp])

        if cap_interval != 0 and tick % cap_interval == 0:
            autocap = threading.Thread(target=capture, args=("auto",), daemon=False)
            acapThreads.append(autocap)
            autocap.start()
        
        if bk_interval != 0 and tick % bk_interval == 0:
            backups = threading.Thread(target=bkACAP, args=(filename))
            acapThreads.append(backups)
            backups.start()

        # This block ensures that the requested tick rate is accurate by
        # factoring in how long it took for the tick to process before
        # sleeping.
        if (time() - startTime) >= poll_interval:
            logging.debug("ACAP tick took longer than prescribed tick time!")
        else:
            sleep(poll_interval-(time()-startTime))
        tick += 1
        
    logging.info("Automatic data capture has ended.")
    return

def bkACAP(filename):
    # Backs up ACAP capture files to guard against data loss.
    srcPath = "{}/{}".format(sessionPath, filename)
    destPath = "{}/{}".format(auxPath, filename)
    os.system("cp {} AUX_{}".format(srcPath, destPath))