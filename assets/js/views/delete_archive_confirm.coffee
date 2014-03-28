SpeakerMotion.Views.DeleteArchiveConfirm = SpeakerMotion.Views.BaseView.extend
    className: "colorboxed-form"
    template: "#delete-archive-confirm-templ"

    events:
        "click #archive": "onClickArchive"
        "click #confirm": "onClickConfirm"

    initialize: (options) ->
        @name = options.name
        @on_archive = options.on_archive
        @on_delete = options.on_delete

    context: ->
        name: @name

    onClickArchive: ->
        @on_archive()
        $.colorbox.close()

    onClickConfirm: ->
        @on_archive()
        $.colorbox.close()
