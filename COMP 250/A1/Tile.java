package BeeShit;

public class Tile {
    private int food;
    private boolean beeHive;
    private boolean hornetNest;
    private boolean onPathToHive;
    private Tile nextTileToHive;
    private Tile nextTileToNest;
    private HoneyBee beeOnTile;
    private SwarmOfHornets swarmOnTile;

    public Tile() {
        food = 0;
        beeHive = false;
        hornetNest = false;
        onPathToHive = false;
        nextTileToHive = null;
        nextTileToNest = null;
        beeOnTile = null;
        swarmOnTile = new SwarmOfHornets();

    }

    public Tile(int food, boolean beeHive, boolean hornetNest, boolean onPathToHive, Tile nextTileToHive,
                Tile nextTileToNest, HoneyBee beeOnTile, SwarmOfHornets swarmOnTile) {
        this.food = food;
        this.beeHive = beeHive;
        this.hornetNest = hornetNest;
        this.onPathToHive = onPathToHive;
        this.nextTileToHive = nextTileToHive;
        this.nextTileToNest = nextTileToNest;

        this.beeOnTile = beeOnTile;
        if (beeOnTile.getPosition() != null) {
            beeOnTile.getPosition().removeInsect(beeOnTile);
            beeOnTile.setPosition(this);
        }
        beeOnTile.setPosition(this); //changes field of BeeShit.HoneyBee upon specific initialization

        this.swarmOnTile = swarmOnTile;
        if (swarmOnTile.sizeOfSwarm() != 0) { //also modifies field of Hornets upon being added
            for (int i = 0; i < swarmOnTile.sizeOfSwarm(); i++) {
                addInsect(swarmOnTile.getHornets()[i]);
            }

        }

    }

    public boolean isHive() {
        return this.beeHive;
    }

    public boolean isNest() {
        return this.hornetNest;
    }

    public void buildHive() {
        this.beeHive = true;
    }

    public void buildNest() {
        this.hornetNest = true;
    }

    public boolean isOnThePath() {
        return this.onPathToHive;
    }

    public Tile towardTheHive() {
        if (this.onPathToHive) {
           return this.nextTileToHive;
        }

        return null;
    }

    public Tile towardTheNest() {
        if (this.onPathToHive) {
            return this.nextTileToNest;
        }

        return null;
    }

    public void createPath(Tile nextTileToHive, Tile nextTileToNest) {
        try {
            nextTileToNest.setNextTileToHive(this);
            nextTileToHive.setNextTileToNest(this);

            this.nextTileToHive = nextTileToHive;
            this.nextTileToNest = nextTileToNest;

            this.onPathToHive = true;
        } catch (Exception e) {

            this.nextTileToHive = nextTileToHive;
            this.nextTileToNest = nextTileToNest;

            this.onPathToHive = true;
        }
    }

    public int collectFood() {
        int foodToReturn = this.food;
        this.food = 0;

        return foodToReturn;
    }

    public void storeFood(int food) {
        this.food += food;
    }

    public HoneyBee getBee() {
        return this.beeOnTile;
    }

    public Hornet getHornet() {
        return this.swarmOnTile.getFirstHornet();
    }

    public int getNumOfHornets() {
        return this.swarmOnTile.sizeOfSwarm();
    }

    public boolean addInsect(Insect insect) { //slapping myself apparently
        if (insect instanceof HoneyBee) {
            if (beeOnTile != null || hornetNest) {
                return false; //if bee already on tile or on nest
            }
            beeOnTile = (HoneyBee) insect;
            insect.setPosition(this); //modifies BeeShit.HoneyBee field
            return true;
        }

        //if insect instanceof BeeShit.Hornet
        else if ((hornetNest || beeHive || onPathToHive)) {
            swarmOnTile.addHornet((Hornet) insect);
            insect.setPosition(this); //modifies BeeShit.Hornet field
            return true;

        }
        return false; //will reach if BeeShit.Hornet doesn't meet criteria
    }

    public boolean removeInsect(Insect insect) {
        Tile insectPosition = insect.getPosition();

        if (insectPosition == this) {
            try {
                this.swarmOnTile.removeHornet((Hornet) insect);
                insect.setPosition(null);
                return true;
            }
            catch (ClassCastException otherInsect) { //bees won't be able to case to hornets
                this.beeOnTile = null;
                insect.setPosition(null);
                return true;
            }
        }
        return false;
    }

    private void setNextTileToHive(Tile tile) {
        this.nextTileToHive = tile;
    }

    private void setNextTileToNest(Tile tile) {
        this.nextTileToNest = tile;
    }


}
