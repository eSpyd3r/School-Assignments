package BeeShit;

public class BusyBee extends HoneyBee {
    public BusyBee(Tile position) {
        super(position, 5, 2);

    }
    public boolean takeAction() {
        this.getPosition().storeFood(2);
        return true;
    }
}
