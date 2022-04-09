import os

class Gathering:
    @property
    def members(self):
        with open("member_list.txt", "r") as member_list:
            member_list = member_list.readlines()
            cleaned_member_list = []
            for member in member_list:
                if member[-1] == "\n":
                    member = member[:-1]
                cleaned_member_list.append(member)
            return  cleaned_member_list

    def show_members(self):
        if len(self.members) > 0:
            return "Number of members: {} \n".format(len(self.members)) + "List of members: \n- {}".format("\n- ".join(meeting.members))
        else:
            return "~ Empty ~"

    def add_member(self, new_member):
        if new_member != " " or new_member != "\n":
            with open("member_list.txt", "a") as member_list:
                member_list.write(new_member+"\n")
        return

    def remove_member(self, member_to_remove):
        can_remove = False
        with open("member_list.txt", "r") as member_list:
            member_list = member_list.readlines()
            for member in member_list:
                if member_to_remove == member or member_to_remove+"\n" == member:
                    member_list.remove(member)
                    updated_member_list = member_list
                    can_remove = True

        if can_remove:
            with open("member_list.txt", "w") as member_list:
                member_list.write("".join(updated_member_list))
        else:
            raise ValueError("list members does not contain member '{}'".format(member_to_remove))
        return 

    def clear_members(self):
        with open("member_list.txt", "w") as member_list:
            member_list.write("")
        return

    @property
    def probability_of_single(self):
        return "1/{}".format(len(self.members))


meeting = Gathering()
while True:
    os.system("clear")
    print("1) View members")
    print("2) Add member")
    print("3) Remove member")
    print("4) Clear members")
    print("5) Gathering stats")
    print("\n99) Quit")
    print("-"*25)

    action = input("\nSelect an option\n> ")

    try:
        action = int(action)
    except ValueError:
        os.system("clear")
        print("Invalid option")
        input("\nRETURN to continue")
        continue


    if action == 1:  # view members
        os.system("clear")
        print(meeting.show_members())
        input("\nRETURN to continue")


    elif action == 2:  # add member
        os.system("clear")
        print(meeting.show_members())
        new_member = input("\nAdd a member:  ")
        meeting.add_member(new_member)
        print("Member added")
        input("\nRETURN to continue")


    elif action == 3:  # remove member
        os.system("clear")
        print(meeting.show_members())
        member_to_remove = input("\nRemove a member:  ")
        meeting.remove_member(member_to_remove)
        print("Member removed")
        input("\nRETURN to continue")

    elif action == 4:  # clear members
        os.system("clear")
        meeting.clear_members()
        input("\nRETURN to continue")


    elif action == 99:
        quit("Goodbye :)")
