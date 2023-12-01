package BeeShit;

public class SwarmOfHornets {
    private Hornet[] swarm;
    private int size;

    public SwarmOfHornets(){
        this.size = 0;
        this.swarm = new Hornet[size];
    }

    public int sizeOfSwarm() {
        int hornetsInSwarm = 0;
        try {
            for (int i = 0; i < size; i ++) {
                if (swarm[i] != null) {
                    hornetsInSwarm++;
                }
            }
        } catch (ArrayIndexOutOfBoundsException ex) { //in case of empty swarm  array
            return 0;
        }

       return hornetsInSwarm;

    }

    public Hornet[] getHornets() {
        int hornetsInSwarm = sizeOfSwarm();
        Hornet[] arrayOfHornets = new Hornet[hornetsInSwarm];

        for (int new_i = 0; new_i < hornetsInSwarm; new_i ++) {
            for (int i = 0; i < size; i++) {
                if (swarm[i] != null) {
                    arrayOfHornets[new_i] = swarm[i];
                    break;
                }
            }
        }


        return arrayOfHornets;

    }

    public Hornet getFirstHornet() {
        Hornet[] arrayOfHornets = getHornets();
        try {
            if (arrayOfHornets[0] != null) {
                return arrayOfHornets[0];
            }
        } catch (ArrayIndexOutOfBoundsException ex) {
            return null;
        }
        return null;
    }

    public void addHornet(Hornet newHornet) {

        if (sizeOfSwarm() == 0) {
            this.size = 1;
            this.swarm = new Hornet[1];
        }

        boolean spaceInSwarm = false;
        for (int i = 0; i < size; i++) {
            if (swarm[i] == null) {
                spaceInSwarm = true;
                swarm[i] = newHornet;
                break;
                }
            }



        if (!spaceInSwarm) {
            Hornet[] newSwarm = new Hornet[size + 1];

            for (int i = 0; i < size; i++) {
                newSwarm[i] = swarm[i];
            }
            newSwarm[newSwarm.length - 1] = newHornet;

            swarm = newSwarm;
            size++;
        }
    }

    public boolean removeHornet(Hornet hornet) {
         if (size != 0) {
             System.out.println(size);
             for (int i = 0; i < size; i++) {
                 if (swarm[i] == hornet) {
                     swarm[i] = null;
                     swarm = getHornets();
                     break;

                 }
             }
             size--;
             return true;
         }
        return false;
    }
}
