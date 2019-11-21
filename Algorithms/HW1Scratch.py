from enum import Enum
import random


class Breed(Enum):
    herd = 0
    retr = 1
    toy = 2


def pull_front(dogs, target, ignore):
    def swap(i, j):
        temp = dogs[i]
        dogs[i] = dogs[j]
        dogs[j] = temp

    front, probe = 0, 0

    while probe < len(dogs):
        current_dog = dogs[front]
        if not (current_dog in target or current_dog in ignore):
            while dogs[probe] not in target:
                probe += 1

                if probe >= len(dogs):
                    return dogs

            swap(front, probe)

        front += 1
        probe = max(front, probe)

    return dogs


def dog_sort(dogs):
    partial = pull_front(dogs, [Breed.herd], [])
    return pull_front(partial, [Breed.retr], [Breed.herd])


def test():
    # generates a dog of random breed
    def random_breed():
        return Breed(random.randint(0, 2))

    # for all consecutive pairs, the list increases
    def check(dogs):
        for pair in zip(dogs, dogs[1:]):
            if pair[0].value > pair[1].value:
                return False

        return True

    # tests lists of increasing size
    for i in range(5, 5005, 50):
        rand = [random_breed() for _ in range(i)]
        run = dog_sort(rand)
        if not check(run):
            print("Failure!")
            print(rand)
            print(run)
            return

    print("Success!")


if __name__ == '__main__':
    test()
