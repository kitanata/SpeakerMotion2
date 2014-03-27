SpeakerMotion.Views.BaseView = Backbone.View.extend

    render: ->
        console.log "BaseView::render Called"
        if @_ctemplate == undefined
            @_ctemplate = Handlebars.compile($(@template).html())

        @$el.html(@_ctemplate(@context()))
        @

    invalidate: ->
        console.log "BaseView::invalidate Called"
        if not @shouldRender
            setTimeout =>
                @beforeRender()
                @render()
                @afterRender()
                @shouldRender = false
            , 500
            @shouldRender = true

    beforeRender: ->

    afterRender: ->

    context: ->
        {}
