from MyRNG import MyRandom
from util import Stack, Queue  # These may come in handy


class User:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

        self.addCalls = 0

    def avgFriendshipsPerUser(self):
        allFriendships = []
        for user in sg.friendships:
            for friend in sg.friendships[user]:
                allFriendships.append(friend)
        return len(allFriendships) / len(sg.users)

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)
            self.addCalls += 1

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}

        rng = MyRandom()
        print("rng seed: ", rng.seed)

        # Add users
        for i in range(num_users):
            self.add_user(f"User {i + 1}")

        while self.avgFriendshipsPerUser() < avg_friendships:
            userID = rng.randomChoice(self.users)
            potentialFriendKey = rng.randomChoice(self.users)
            while potentialFriendKey == userID or potentialFriendKey in self.friendships[userID]:
                potentialFriendKey = rng.randomChoice(self.users)
            self.add_friendship(userID, potentialFriendKey)

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set

        q = Queue()
        q.enqueue([user_id])

        while q.size() > 0:
            path = q.dequeue()
            otherUser = path[-1]

            if otherUser not in visited:
                visited[otherUser] = path
                for friend in self.friendships[otherUser]:
                    newPath = path.copy()
                    newPath.append(friend)
                    q.enqueue(newPath)

        return visited

    def averageDegreeOfSeparation(self, userID):
        allPaths = self.get_all_social_paths(userID)
        totalDegrees = 0
        totalPaths = len(allPaths)
        print(f"total paths for {userID}: {totalPaths}")
        for path in allPaths:
            totalDegrees += len(allPaths[path])
        return totalDegrees / totalPaths

if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)
