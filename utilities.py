
def getNoJobsMoved(old_distribution, new_distribution):
    noMovement = []
    for entry in old_distribution:
        if entry in new_distribution:
            oldJobList = old_distribution[entry]
            newJobList = new_distribution[entry]
            for i in oldJobList:
                if i in newJobList:
                    continue
                else:
                    break
            if i ==  oldJobList[-1] and  i in newJobList:
                 noMovement.append(entry)
    return noMovement

