SpeakerMotion.Layouts.Index = SpeakerMotion.Views.BaseView.extend
    template: "#index-templ"

    initialize: (options) ->
        @shouldRender = false
        @invalidate()

    userLoggedIn: ->
        user != null

    context: ->
        {}
