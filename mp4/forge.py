import os
import glob
import click

from pxyz.models import Tag, Item, User, Role

admin = os.getenv('PXYZ_ADMIN', "Admin")
password = os.getenv('PXYZ_ADMIN_PASSWORD', 'helloadmin')

roles_permissions_map = {
    'Locked': ['FOLLOW', 'COLLECT'],
    'User': ['FOLLOW', 'COLLECT', 'COMMENT', 'UPLOAD'],
    'Moderator': ['FOLLOW', 'COLLECT', 'COMMENT', 'UPLOAD', 'MODERATE'],
    'Administrator': ['FOLLOW', 'COLLECT', 'COMMENT', 'UPLOAD', 'MODERATE', 'ADMINISTER']
}
single_file_tags = ['txt', 'epub', 'mp4']
multi_files_tags = ['pics', 'songs']

def add_upload_item(upload_dir, tag):
    item_paths = glob.glob(os.path.join(upload_dir, tag, '*.'+tag))
    item_names = [os.path.basename(f).split('.')[0] for f in item_paths]
    for item in item_names:
        Item.add_item(tag, item, admin)
    click.echo('add '+tag)

def add_upload_items(upload_dir, tag, format=''):
    item_dict = {}
    items_paths = glob.glob(os.path.join(upload_dir, tag, '*.jpg'))
    item_names = ['.'.join(os.path.basename(f).split('.')[:-1]) for f in items_paths]
    for item in item_names:
        multi_paths = glob.glob(os.path.join(upload_dir, tag, item, '*'+format))
        multi_names = [os.path.basename(f) for f in multi_paths]
        item_dict[item] = multi_names
    Item.add_item_dict(tag, item_dict, admin)
    click.echo('add '+tag)


def gen_all(app):
    upload_dir = app.config['PXYZ_UPLOAD_PATH']

    Role.add_roles(roles_permissions_map)
    click.echo('add the roles and permissions')

    Tag.add_tags(single_file_tags)
    Tag.add_tags(multi_files_tags)
    click.echo('add tags')

    User.add_user(os.getenv('PXYZ_ADMIN'), os.getenv('PXYZ_ADMIN_PASSWORD'), 'Administrator')
    click.echo('add admin')

    for tag in single_file_tags:
        add_upload_item(upload_dir, tag)

    add_upload_items(upload_dir, 'songs', '.mp3')

    add_upload_items(upload_dir, 'pics')



