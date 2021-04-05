
PIPELINE_CSS = {
    'bootstrap': {
        'source_filenames': (
            'twitter_bootstrap/less/bootstrap.less',
        ),
        'output_filename': 'css/b.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
}

PIPELINE_JS = {
    'bootstrap': {
        'source_filenames': (
            'twitter_bootstrap/js/transition.js',
            'twitter_bootstrap/js/modal.js',
            'twitter_bootstrap/js/dropdown.js',
            'twitter_bootstrap/js/scrollspy.js',
            'twitter_bootstrap/js/tab.js',
            'twitter_bootstrap/js/tooltip.js',
            'twitter_bootstrap/js/popover.js',
            'twitter_bootstrap/js/alert.js',
            'twitter_bootstrap/js/button.js',
            'twitter_bootstrap/js/collapse.js',
            'twitter_bootstrap/js/carousel.js',
            'twitter_bootstrap/js/affix.js',
        ),
        'output_filename': 'js/b.js',
    },
}

PIPELINE_COMPILERS = (
    'pipeline.compilers.less.LessCompiler',
)

PIPELINE = {
    'PIPELINE_ENABLED': True,
    'JAVASCRIPT': PIPELINE_JS,
    'STYLESHEETS': PIPELINE_CSS
}
