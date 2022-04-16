"""
Generates json files for minecraft modding
Also made for personal use :)
"""

import json
import sys
import os
import shutil


def make_files(to_change, item_name, mod_id, texture_id):
    """makes all the files."""
    for to_make in to_change:
        with open(f"templates/{to_make}.json", encoding="UTF-8") as file_with:
            template_json = file_with.read()

            to_make_list = to_make.split('/')
            dir_for_file = 'out/' + '/'.join(to_make_list[0:-1])
            file_name = f"{dir_for_file}/{to_make_list[-1].replace('common', item_name)}.json"

            new_json = make_new_json(
                template_json, mod_id, texture_id, item_name)

            make_dir(dir_for_file)
            with open(file_name, 'a', encoding="UTF_8") as file_with:
                file_with.write(new_json)


def make_dir(dirs):
    """makes directory"""
    try:
        os.makedirs(dirs)
    except FileExistsError:
        pass


def make_new_json(got_json, mod_id, texture_id, item_name):
    """Returns new json"""
    return got_json.replace(
        'MODID', mod_id).replace('TEXTUREID', texture_id).replace('common', item_name)


def main():
    '''Main function to do all the job.'''
    shutil.rmtree("out/", ignore_errors=True)

    #! if block modle is not created, the slab blockstate would not work.
    with open("config.json", encoding="UTF-8") as file_with:
        config_content = json.loads(file_with.read())
    #   Which mode ex: stairs to generate stair.
    #   If wanted all, use all (refer modes.json for those).
        mode_to_use = input(": ")
        item_name = dict(config_content).get("item_name")
        texture_id = config_content.get("texture_id")
        mod_id = config_content.get("mod_id")

    with open("modes.json", encoding='UTF-8') as file_with:
        modes = json.loads(file_with.read())

    modes_possible_to_use = modes.keys()

    if not mode_to_use in modes_possible_to_use:
        sys.exit()  # will be changed to return

    if mode_to_use in ('*', "all"):
        for i in list(modes_possible_to_use)[2:]:
            make_files(modes[i], item_name, mod_id, texture_id)
    else:
        files_to_change = modes[mode_to_use]
        make_files(files_to_change, item_name, mod_id, texture_id)

    print("Done. :)")


if __name__ == "__main__":
    main()
