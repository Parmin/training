#include <iostream>
#include <mongocxx/client.hpp>
#include <mongocxx/cursor.hpp>
#include <mongocxx/collection.hpp>
#include <bsoncxx/builder/stream/document.hpp>
#include <bsoncxx/builder/concatenate.hpp>
#include <bsoncxx/builder/basic/kvp.hpp>
#include <mongocxx/exception/exception.hpp>
#include <mongocxx/exception/operation_exception.hpp>
#include <mongocxx/insert_many_builder.hpp>
#include <bsoncxx/json.hpp>

using namespace bsoncxx::builder::stream;
using namespace bsoncxx::types;
using namespace mongocxx;

void comparission_operators(){
  // instantiate a connection
  client conn{mongocxx::uri{}};
  //instantiate a collection
  collection coll = conn["sample"]["movies"];
  document query;

  query << "imdb_rating" << open_document << "$gte" << 7 << close_document;
  query << "category" << open_document << "$ne" << "family" << close_document;
  query << "category" << open_document << "$in"
    << open_array << "Batman" << "Godzilla" << close_array
  << close_document;

  coll.find( query.view() );
}

void logical_operators(){
  // instantiate a connection
  client conn{mongocxx::uri{}};
  //instantiate a collection
  collection coll = conn["sample"]["movies"];


  document query;

  query << "$or"
    << open_array
      << open_document << "category" << "sci-fi" << close_document
      << open_document << "imdb_rating"
        << open_document << "$gte" << 7 << close_document
      << close_document
    << close_array;


  document category_scifi, category_family;
  category_scifi << "category" << "sci-fi"
    << "imdb_rating" << open_document  << "$gte" << 8 << close_document;
  category_family << "category" << "sci-fi"
    << "imdb_rating" << open_document  << "$gte" << 7 << close_document;

  b_document or1{category_scifi.view()};
  b_document or2{category_family.view()};

  query << "$or"
  << open_array
    << or1 << or2
  << close_array;

  query << "imdb_rating"
    << open_document << "$not"
      << open_document << "$gt" << 7 << close_document
    << close_document;



  coll.find( query.view() );
}


void element_operators(){
  // instantiate a connection
  client conn{mongocxx::uri{}};
  //instantiate a collection
  collection coll = conn["sample"]["movies"];

  // basic builder
  using bsoncxx::builder::basic::kvp;
  auto query = bsoncxx::builder::basic::document{};
  query.append(kvp( "budget", kvp("$exists", true)  ));

  coll.find(query.view());

}


int main(int, char**) {
    try{
      logical_operators();
    } catch( const exception &e ) {
      std::cout << "caught " << e.what() << std::endl;
    }
    return EXIT_SUCCESS;

}
