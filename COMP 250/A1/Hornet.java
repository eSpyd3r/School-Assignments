package BeeShit;

public class Hornet extends Insect {
    private int atk;

    public Hornet(Tile position, int hp, int atk) {
        super(position, hp);
        this.atk = atk;
    }

    public boolean takeAction() {
        if (this.getPosition() == null) {
            return false; //dead hornet can't move?
        }

        if (this.getPosition().getBee() != null) {
            this.getPosition().getBee().takeDamage(atk);
            return true;
        }
        else if (this.getPosition().isHive()) {
            return false;
        }
        else {
            Tile newPosition = this.getPosition().towardTheHive();
            System.out.println("yeehaw");
            this.getPosition().removeInsect(this);
            newPosition.addInsect(this);
            return true;
        }

    }

    public boolean equals(Object obj) {
        return (obj instanceof Hornet && ((Hornet) obj).getHealth() == this.getHealth() &&
                ((Hornet) obj).getPosition() == this.getPosition());
    }


}
