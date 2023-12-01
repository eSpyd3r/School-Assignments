package BeeShit;

public class TankyBee extends HoneyBee {
    private int atk;
    private int armor;

    public TankyBee(Tile position, int atk, int armor) {
        super(position, 30, 3);
        this.atk = atk;
        this.armor = armor;

    }

    public boolean takeAction() {
        if (this.getPosition().getNumOfHornets() != 0) {
            this.getPosition().getHornet().takeDamage(atk);
            return true;
        }

        else {
            return false;
        }
    }

    public void takeDamage(int dmg) {
        double multiplier = (double)100/(100 + armor);
        double tankyDmg = multiplier * dmg;

        super.takeDamage((int)tankyDmg);

    }

    public boolean equals(Object obj) {
        return (obj instanceof TankyBee && ((TankyBee) obj).getHealth() == this.getHealth() &&
                ((TankyBee) obj).getPosition() == this.getPosition());
    }
}
