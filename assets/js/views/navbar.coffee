SpeakerMotion.Views.NavBar = SpeakerMotion.Views.BaseView.extend
    template: "#navbar-templ"

    events:
        "click #login": "onClickLogin"
        "click #register": "onClickRegister"

    initialize: (options) ->
        if user
            @listenTo(user, 'change', @render)

    render: ->
        source = $(@template).html()
        template = Handlebars.compile(source)

        @$el.html(template(@context()))
        @

    invalidate: ->
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

    userLoggedIn: ->
        user != null

    userIsStaff: ->
        user != null and user.get('is_staff') == true

    userOwnsContent: ->
        user != null and user.id == @model.get('speaker').id

    userIsEventPlanner: ->
        user != null and user.get('is_event_manager')

    userProfileLink: ->
        if user == null
            console.log "USER IS NULL"
            ""
        else
            console.log "LEGIT"
            console.log user.get('url')
            user.get('url')

    context: ->
        userLoggedIn: @userLoggedIn()
        userIsStaff: @userIsStaff()
        userIsEventPlanner: @userIsEventPlanner()
        profileLink: @userProfileLink()

    onClickLogin: ->
        loginModel = new SpeakerMotion.Models.Login()
        console.log loginModel

        editor = new SpeakerMotion.Views.Login
            model: loginModel

        console.log editor

        $.colorbox
            html: editor.render().el
            width: "300px"
            height: "440px"
        $.colorbox.resize()

    onClickRegister: ->
        console.log "onClickRegister"
        regModel = new SpeakerMotion.Models.Register()

        editor = new SpeakerMotion.Views.Register
            model: regModel

        console.log regModel
        console.log editor

        $.colorbox
            html: editor.render().el
            width: "300px"
            height: "440px"
        $.colorbox.resize()
