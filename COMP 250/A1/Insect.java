package BeeShit;

abstract class Insect {
    private Tile position;
    private int hp;

    public Insect(Tile position, int hp) {
        if (this instanceof HoneyBee && (position.getBee() != null && position.getBee() != this)) {
            throw new IllegalArgumentException();
        }
        else {
            this.position = position;
            this.hp = hp;

            position.addInsect(this); //adds the insect to given position
        }

    }

    public final Tile getPosition() {
        return this.position;
    }

    public final int getHealth() {
        return this.hp;
    }

    public void setPosition(Tile position) {
        this.position = position;
    }

    public void takeDamage(int dmg) {
        if (this instanceof HoneyBee && position.isHive()) {
            dmg = (int) (dmg * 0.9);
        }
        hp = hp - dmg;

        if (hp <= 0) {
            System.out.println("mf died lmao");
            position.removeInsect(this);

        }
    }

    public abstract boolean takeAction();

    public boolean equals(Object obj) {
        return (obj instanceof Insect && ((Insect) obj).getHealth() == this.getHealth() &&
                ((Insect) obj).getPosition() == this.getPosition());
    }

}
