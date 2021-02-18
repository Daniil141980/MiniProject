from showMap import show_map


def main():
    lat = 55.729738
    lon = 37.664777
    z = 10
    ll_z = f'll={lon},{lat}&z={z}'
    show_map(ll_z)


if __name__ == '__main__':
    main()
