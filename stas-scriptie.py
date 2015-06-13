import json

import click
import praw
import requests
from lxml import etree

from lib import config

USER_AGENT = 'python ({requester}):stas-scriptie:0.0.1 (by /u/MrJohz)'

@click.group(chain=True)
@click.pass_context
@click.option('--envfile', default=None)
def cli(ctx, envfile):
    ctx.obj['config'] = config.Config(envfile)
    ctx.obj['stored-data'] = config.StoredData(ctx.obj['config'].filename)

    uagent = ctx.obj['config'].get('user_agent', default=USER_AGENT)

    ctx.obj['requests'] = requests.Session()
    ctx.obj['requests'].headers.update({'User-Agent': uagent.format(requester='requests')})
    ctx.obj['reddit'] = praw.Reddit(uagent.format(requester='praw'))

@cli.command()
@click.pass_context
def update_admins(ctx):
    admin_text = ctx.obj['requests'].get('http://www.reddit.com/about/team').text
    admin_html = etree.HTML(admin_text)
    script = admin_html.findall('.//script')[-2]

    data = json.loads(script.text[14:-2])  # NOTE: This is liable to breaking

    ctx.obj['stored-data'].team = data['#team']
    ctx.obj['stored-data'].alumni = data['#alumni']

@cli.command()
@click.pass_context
def download(ctx):
    ctx.obj['config'].filename

if __name__ == "__main__":
    cli(obj={})
