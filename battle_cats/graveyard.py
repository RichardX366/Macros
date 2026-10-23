from battle_cats.superior import (
    attempt_run,
    click_cat,
    click_upgrade,
    level,
    cat_counts,
)


def run(upgrade: bool, cats: list[bool]):
    if cat_counts[8] > 0 and cat_counts[9] > 0:
        if cats[8]:
            click_cat(8)
        elif cats[7]:
            click_cat(7)
        elif cats[9]:
            click_cat(9)
        elif cats[3]:
            click_cat(3)
        elif cats[4]:
            click_cat(4)
        elif level[0] < 8 and upgrade:
            click_upgrade()
        elif cats[6]:
            click_cat(6)
        elif cats[5]:
            click_cat(5)
        return

    if cats[8]:
        click_cat(8)
    elif cats[9]:
        click_cat(9)
    elif cats[3]:
        click_cat(3)
    elif cats[4]:
        click_cat(4)
    elif level[0] < 4 and upgrade:
        click_upgrade()


if __name__ == "__main__":
    attempt_run(run)
