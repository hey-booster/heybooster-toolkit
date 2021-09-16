""" Update Version Script """
with open("version.txt", "r") as version_file:
    version = version_file.read()
    version_numbers = version.split(".")

    version_numbers[-1] = str(int(version_numbers[-1]) + 1)
    new_version = ".".join(version_numbers)

with open("version.txt", "w") as version_file:
    version_file.write(new_version)