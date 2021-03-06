SpkrBar.Views.ProfileTalk = Backbone.View.extend
    className: "talk_event"
    template: "#profile-talk-templ"

    events:
        "click .endorse-talk": "onClickEndorseTalk"

    initialize: (options) ->
        @listenTo(@model, "change", @render)
        @listenTo(@model.get('endorsements'), "add remove change reset", @render)

        @model.fetchRelated('endorsements')

    render: ->
        source = $(@template).html()
        template = Handlebars.compile(source)

        @$el.html(template(@context()))
        @

    userLoggedIn: ->
        user != null

    userOwnsContent: ->
        speaker = @model.get('speaker')
        user != null and speaker != null and user.id == speaker.id

    context: ->
        id: @model.id
        name: @model.get('name')
        abstract: _.str.stripTags(markdown.toHTML(@model.get('abstract')))
        url: '/talk/' + @model.get('id')
        endorsed: @model.userEndorsed()
        userLoggedIn: @userLoggedIn()
        userOwnsContent: @userOwnsContent()

    onClickEndorseTalk: (el) ->
        newEndorsement = new SpkrBar.Models.TalkEndorsement
            talk: @model
            user: user
        newEndorsement.save null,
            success: =>
                @model.get('endorsements').add newEndorsement
