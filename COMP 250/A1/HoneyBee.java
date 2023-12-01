package BeeShit;

abstract class HoneyBee extends Insect {
    private int foodCost;

    public HoneyBee(Tile position, int hp, int foodCost) {
        super(position, hp);
        this.foodCost = foodCost;
    }

    public int getCost() {
        return this.foodCost;
    }

    public boolean equals(Object obj) {
        return (obj instanceof HoneyBee && ((HoneyBee) obj).getHealth() == this.getHealth() &&
                ((HoneyBee) obj).getPosition() == this.getPosition());
    }
}
