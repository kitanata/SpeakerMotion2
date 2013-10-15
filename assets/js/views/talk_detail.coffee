SpkrBar.Views.TalkDetail = Backbone.View.extend
    template: "#talk-detail-templ"

    events:
        "click .add-talk-tag": 'onAddTalkTag'
        "click .delete-talk-tag": 'onDeleteTalkTag'
        "click .add-talk-link": 'onAddTalkLink'
        "click .delete-talk-link": 'onDeleteTalkLink'
        "click #add-slides": "onClickAddSlides"
        "click #add-videos": "onClickAddVideos"
        "click #add-photos": "onClickAddPhotos"
        "click #edit-talk": "onClickEditTalk"
        "click #delete-talk": "onClickDeleteTalk"
        "click #create-engagement": "onClickCreateEngagement"
        "click #publish-talk": "onClickPublishTalk"
        "click #submit-comment": "onClickSubmitComment"
        "click .delete-slide": "onClickDeleteSlide"
        "click .delete-video": "onClickDeleteVideo"

    initialize: (options) ->
        @shouldRender = false
        @engagementViews = []
        @commentViews = []

        @allTags = new SpkrBar.Collections.TalkTags()
        @tags = new Backbone.Collection()
        @links = new Backbone.Collection()
        @slides = new Backbone.Collection()
        @videos = new Backbone.Collection()
        @engagements = new Backbone.Collection()
        @speaker = new SpkrBar.Models.User()

        @locations = new SpkrBar.Collections.Locations()

        @listenTo(@tags, "change add remove reset", @invalidate)
        @listenTo(@links, "change add remove", @invalidate)
        @listenTo(@slides, "change add remove", @invalidate)
        @listenTo(@videos, "change add remove", @invalidate)
        @listenTo(@engagements, "change add remove", @buildEngagementViews)
        @listenTo(@model, "change", @invalidate)
        @listenTo(@speaker, "change", @invalidate)

        @locations.fetch
            success: =>
                @fetchTalkTags => 
                    @fetchTalkDetailModel()

    fetchTalkTags: (next) ->
        @allTags.fetch
            success: => 
                next()

    fetchTalkDetailModel: ->
        engagements = @model.get 'engagements'
        links = @model.get 'links'
        slides = @model.get 'slides'
        videos = @model.get 'videos'
        comments = @model.get 'comments'

        @speaker.id = @model.get('speaker')
        @speaker.fetch()

        _(engagements).each (x) =>
            engagementModel = new SpkrBar.Models.Engagement
                id: x
            engagementModel.fetch
                success: =>
                    @engagements.add engagementModel

        tagIds = @model.get('tags')
        @tags.reset(@allTags.filter (x) => x.id in tagIds)

        _(links).each (x) =>
            linkModel = new SpkrBar.Models.TalkLink
                id: x
            linkModel.fetch
                success: =>
                    @links.push linkModel

        _(slides).each (x) =>
            slideModel = new SpkrBar.Models.TalkSlideDeck
                id: x
            slideModel.fetch
                success: =>
                    @slides.push slideModel

        _(videos).each (x) =>
            videoModel = new SpkrBar.Models.TalkVideo
                id: x
            videoModel.fetch
                success: =>
                    @videos.push videoModel

        @model.get('comments').fetch
            success: =>
                console.log "callback"
                @model.get('comments').each (x) =>
                    commenter = new SpkrBar.Models.User
                        id: x.get('commenter')

                    commenter.fetch
                        success: =>
                            commentView = new SpkrBar.Views.Comment
                                parent: @
                                model: x 
                                commenter: commenter
                            @commentViews.push commentView

    render: ->
        console.log "Render"
        source = $(@template).html()
        template = Handlebars.compile(source)

        @$el.html(template(@context()))
        @

    invalidate: ->
        console.log "Invalidate"
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
        console.log "AfterRender"
        _(@engagementViews).each (enView) =>
            $('#engagement-list-region').append enView.render().el

        _(@commentViews).each (comView) =>
            $('.root-comment-list').append comView.render().el

    buildEngagementViews: ->
        console.log "buildEngagementViews"
        @engagementViews = []
        $('#engagement-list-region').html('')

        @engagements.each (x) =>
            newView = new SpkrBar.Views.Engagement
                model: x
                talk: @model
                location: @locations.find (y) => y.id == x.get('location')
            @engagementViews.push(newView)
        @invalidate()

    userLoggedIn: ->
        user != null

    userOwnsContent: ->
        user != null and user.id == @speaker.id

    userEndorsed: ->
        if user == null
            return false
        else
            user.id in @model.get('endorsements')

    userRated: ->
        user.id in @model.get('ratings')

    showTags: ->
        @tags.length != 0 or @userOwnsContent()

    showLinks: ->
        @links.length != 0 or @userOwnsContent()

    context: ->
        id: @model.id
        userLoggedIn: @userLoggedIn()
        userOwnsContent: @userOwnsContent()
        userEndorsed: @userEndorsed()
        numEndorsements: @model.get('endorsements').length
        published: @model.get('published')
        speakerName: @speaker.get('full_name')
        speakerUrl: @speaker.get('url')
        name: @model.get('name')
        abstract: markdown.toHTML(@model.get('abstract'))
        photo: @speaker.get('photo')
        slides: @slides.map (x) -> {'id': x.id, 'embed_code': x.get('embed_code')}
        videos: @videos.map (x) -> {'id': x.id, 'embed_code': x.get('embed_code')}
        showTags: @showTags()
        showLinks: @showLinks()
        tags: @tags.map (x) -> {'id': x.id, 'tag': x.get('name')}
        links: @links.map (x) -> {'id': x.id, 'name': x.get('name'), 'url': x.get('url')}

    deleteComment: (comView) ->
        @commentViews = _(@commentViews).without comView
        comView.model.destroy()
        @invalidate()

    onAddTalkTag: ->
        name = $('#new-talk-tag-name').val()

        tag = @allTags.find (x) => x.get('name') == name

        addTagToModel = (tag) =>
            tags = @model.get('tags')
            tags.push tag.id
            @tags.add tag
            @model.set 'tags', tags
            @model.save()

        if tag
            addTagToModel(tag)
        else
            newTags = new SpkrBar.Models.TalkTag
                name: name

            newTag.save null, 
                success: =>
                    addTagToModel(newTag)
                    @allTags.add newTag

    onDeleteTalkTag: (el) ->
        tagId = $(el.currentTarget).data('id')
        tags = _(@model.get('tags')).reject (x) => x == tagId
        @model.set 'tags', tags
        @model.save()

        deadTag = @tags.find (x) => x.id == tagId
        @tags.remove(deadTag)

    onAddTalkLink: ->
        name = $('#new-talk-link-name').val()
        url = $('#new-talk-link-url').val()

        newLink = new SpkrBar.Models.TalkLink
            talk: @model.id
            name: name
            url: url
        newLink.save null, 
            success: =>
                links = @model.get 'links'
                links.push newLink.id
                @model.set 'links', links
                @model.save()
                @links.add newLink

    onDeleteTalkLink: (el) ->
        linkId = $(el.currentTarget).data('id')
        deadLink = @links.find (x) => x.id == linkId

        deadLink.destroy
            success: =>
                @links.remove deadLink
                links = _(@model.get 'links').reject (x) -> x == linkId
                @model.set 'links', links
                @model.save()

    onClickAddSlides: ->
        $.colorbox
            html: $('#link-slides-popup').clone()
            width: "400px"

    onClickDeleteSlide: (el) ->
        slideId = $(el.currentTarget).data('id')

        slide = @slides.find (x) => x.id == slideId
        @slides.remove slide
        slide.destroy()

    onClickAddVideos: ->
        $.colorbox
            html: $('#link-video-popup').clone()
            width: "400px"

    onClickDeleteVideo: (el) ->
        vidId = $(el.currentTarget).data('id')

        video = @videos.find (x) => x.id == vidId
        @videos.remove video
        video.destroy()

    onClickAddPhotos: ->
        $.colorbox
            html: $('#upload-photo-popup').clone()
            width: "400px"

    onClickEditTalk: ->
        editor = new SpkrBar.Views.TalkEdit
            model: @model

        $.colorbox
            html: editor.render().el
            width: "700px"
            height: "520px"

    onClickDeleteTalk: ->
        $.colorbox
            html: $('#delete-talk-popup').clone()
            width: "400px"

    onClickPublishTalk: ->
        @model.set 'published', !(@model.get 'published')
        @model.save()

    onClickCreateEngagement: ->
        createEngagementView = new SpkrBar.Views.CreateEngagement
            talk: @model
            locations: @locations
            parent: @

        $.colorbox
            html: createEngagementView.render().el
            width: "514px"

    onClickSubmitComment: ->
        newComment = new SpkrBar.Models.TalkComment
            talk: @model.id
            commenter: user.id
            comment: $('#comment-area').val()

        newComment.save null,
            success: =>
                commentView = new SpkrBar.Views.Comment
                    parent: @
                    talk: @model
                    model: newComment
                    commenter: user
                @commentViews.push commentView
                @invalidate()
