import mkdocs

class EventsConfig(mkdocs.config.base.Config):

    config_scheme = (
        ('events_dir', mkdocs.config.config_options.Type(str, default='events')),
    )

class EventsPlugin(mkdocs.plugins.BasePlugin[EventsConfig]):
    pass


    