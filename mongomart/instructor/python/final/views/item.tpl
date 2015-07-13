<!DOCTYPE html>
<html lang="en">

    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="description" content="">
        <meta name="author" content="">
        <link rel="icon" href="/img/favicon.ico" type="image/x-icon" />
        <link rel="shortcut icon" href="/img/favicon.ico" type="image/x-icon" />

        <title>{{item['title']}} - MongoMart</title>

        <!-- Bootstrap Core CSS -->
        <link href="/static/css/bootstrap.min.css" rel="stylesheet">

        <!-- Custom CSS -->
        <link href="/static/css/shop-homepage.css" rel="stylesheet">

        <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
        <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
        <!--[if lt IE 9]>
        <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
        <![endif]-->
    </head>

<body>

% # Include navigation
%include('includes/nav.tpl')

<!-- Page Content -->
<div class="container">

    <div class="row">

        <div class="row">
            <div class="col-md-12">
                <ol class="breadcrumb">
                    <li><a href="/">Home</a></li>
                    <li><a href="/?category=${item.category}">{{item['category']}}</a></li>
                    <li class="active">{{item['title']}}</li>
                </ol>
            </div>
        </div>

        <!-- Product Item Heading -->
        <div class="row">
            <div class="col-lg-12">
                <h1 style="margin-top: 0px;" class="page-header">{{item['title']}}
                    <small>{{item['slogan']}}</small>
                </h1>
            </div>
        </div>
        <!-- /.row -->

        <!-- Product Item Row -->
        <div class="row">

            <div class="col-md-8">
                <img class="img-responsive" src="/static/{{item['img_url']}}" alt="">
            </div>

            <div class="col-md-4">
                <h3>Product Description</h3>

                <div class="ratings" style="padding-left: 0px;">
                    <p class="pull-right">{{num_reviews}} reviews</p>
                    <p>

                        % # Display stars
                        
                        %for num in range(1,6):
                            <span class="glyphicon {{'glyphicon-star' if stars >= num else 'glyphicon-star-empty'}}"></span>
                        %end

                    </p>
                </div>

                <p>
                    {{item['description']}}
                </p>

                <a class="btn btn-primary" href="/cart/add?itemid=${item.id}">Add to cart <span class="glyphicon glyphicon-chevron-right"></span></a>

            </div>

        </div>
        <!-- /.row -->

        <!-- Related Products Row -->
        <div class="row">

            <div class="col-lg-12">
                <h3 class="page-header">Latest Reviews</h3>
            </div>

            <div class="col-lg-12">

                %for review in item['reviews']:
                
                    <!-- Comment -->
                    <div>
                        <div>
                            <h4 class="media-heading">{{review['name']}}
                                <small>{{review['date'].strftime('%Y-%m-%d')}}</small>
                            </h4>
                            <div class="ratings" style="padding-left: 0px;">

                                %for num in range(1,6):
                                    <span class="glyphicon {{'glyphicon-star' if review['stars'] >= num else 'glyphicon-star-empty'}}"></span>
                                %end

                            </div>

                            {{review['comment']}}
                        </div>
                    </div>

                    <hr />

                %end 

            </div>

        </div>

        <!-- Comments Form -->
        <div class="well">
            <h4>Add a Review:</h4>
            <form action="/add-review" role="form">
                <input type="hidden" name="itemid" value="{{item['_id']}}" />
                <div class="form-group">
                    <label for="review">Review:</label>
                    <textarea name="review" class="form-control" rows="3"></textarea>
                </div>
                <div class="form-group">
                    <label for="name">Name:</label>
                    <input type="text" class="form-control" id="name" name="name" placeholder="Enter display name">
                </div>
                <div class="form-group">

                    <label class="radio-inline">
                        <input type="radio" name="stars" id="stars" value="1"> 1 star
                    </label>
                    <label class="radio-inline">
                        <input type="radio" name="stars" id="stars" value="2"> 2 star
                    </label>
                    <label class="radio-inline">
                        <input type="radio" name="stars" id="stars" value="3"> 3 star
                    </label>
                    <label class="radio-inline">
                        <input type="radio" name="stars" id="stars" value="4"> 4 star
                    </label>
                    <label class="radio-inline">
                        <input type="radio" name="stars" id="stars" value="5" checked> 5 star
                    </label>
                </div>
                <button type="submit" class="btn btn-primary">Submit Review</button>
            </form>
        </div>

        <hr>

        <!-- Related Products Row -->
        <div class="row">

            <div class="col-lg-12">
                <h3 class="page-header">Related Products</h3>
            </div>

            %for related_item in related_items:
                <div class="col-sm-3 col-xs-6">
                    <a href="/item?id={{related_item['_id']}}">
                        <img class="img-responsive portfolio-item" src="/static/{{related_item['img_url']}}" alt="">
                    </a>
                </div>
            %end

        </div>
        <!-- /.row -->

    </div>

</div>

% # Include footer
%include('includes/footer.tpl')

</body>

</html>
