import click
from flask.cli import with_appcontext
from src.project.extensions import memcachedcache, rediscache, filecache


@click.group()
def health():
    """
    Function to checking services like caches, databases, etc.
    """


@health.command()
@with_appcontext
@click.option(
    "-t",
    "--type",
    "cache_type",
    default="REDIS",
    help="Cache type. Defaults to REDIS. Allows: REDIS, MEMCACHED, FILESYSTEM",
)
def cache(cache_type) -> None:
    """
    Performs a checking against given cache backend.
    """

    cache_backends = {"REDIS": rediscache, "MEMCACHED": memcachedcache, "FILESYSTEM": filecache}

    if cache_type in cache_backends:
        service = cache_backends[cache_type]

        service.set("TEST", "VALUE")
        assert service.get("TEST") == "VALUE"

        service.delete("TEST")
        assert service.get("TEST") is None

        click.echo("OK")
    else:
        click.echo("Invalid cache backend")
