SpeakerMotion.Views.CreateCampaign = SpeakerMotion.Views.BaseView.extend
    className: "campaign-form"
    template: "#create-campaign-templ"

    events:
        "click #submit": "onSubmit"

    initialize: (options) ->
        @alertTempl = Handlebars.compile($('#alert-templ').html())
        @listenTo(@model, "change", @render)

        @success = options.success

    context: ->
        name: @model.get 'name'

    onSubmit: ->
        console.log @model
        console.log @$el.find('#campaign-name').val()
        @model.set
            name: @$el.find('#campaign-name').val()
            manager: user

        if @model.isValid(true)
            @model.save null,
                success: =>
                    @success()
                error: (model, xhr, options) =>
                    error = JSON.parse(xhr.responseText)
                    if error.error == "account_disabled"
                        html = @alertTempl({error: "This account has been disabled. Please contact customer care for help."})
                        $('#alert-area').show()
                        $('#alert-area').append html
                        $.colorbox.resize()
                    else if error.error == "auth_failed"
                        html = @alertTempl({error: "Your username or password is incorrect."})
                        $('#alert-area').show()
                        $('#alert-area').append html
                        $.colorbox.resize()
