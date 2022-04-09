class RAM:
    def __init__(self, address_num):
        # address_num should be a power of 2
        self.addresses = {i: "0" * 8 for i in range(address_num)}
        return

    def get_address(self, address):
        """Return the value at the address specified."""
        data = self.addresses.get(address)
        if data == None:
            raise KeyError("invalid address {}; address not in range".format(address))
        return data

    def store_new(self, address, data):
        """Store data at an address."""
        try:
            self.addresses[address] = data
        except KeyError:
            raise KeyError("invalid address {}; address not in range".format(address))
        return


if __name__ == "__main__":
    ram = RAM(16)
    print(ram.addresses)
    ram.store_new(11, "hello")
