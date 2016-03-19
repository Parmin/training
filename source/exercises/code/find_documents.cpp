#include <iostream>
#include <mongocxx/client.hpp>
#include <mongocxx/cursor.hpp>
#include <mongocxx/collection.hpp>
#include <bsoncxx/builder/stream/document.hpp>
#include <bsoncxx/builder/basic/kvp.hpp>
#include <mongocxx/exception/exception.hpp>
#include <mongocxx/exception/operation_exception.hpp>
#include <mongocxx/insert_many_builder.hpp>
#include <bsoncxx/types.hpp>
#include <bsoncxx/json.hpp>

using namespace bsoncxx::builder::stream;
using namespace mongocxx;


void count_spanish_airlines(){
  // instantiate a connection
  client conn{mongocxx::uri{}};
  // instantiate a collection
  collection coll = conn["air"]["airlines"];
  // create query filter
  document filter;
  filter << "country" << "Spain";

  std::cout << "Spanish Airlines: " << coll.count(filter.view()) << std::endl;
}

void routes_NYC_BARCELONA(){
  // instantiate a connection
  client conn{mongocxx::uri{}};
  // instantiate a collection
  collection coll = conn["air"]["routes"];
  // create query filter
  document filter;
  filter << "src_airport" << open_document
    << "$in" << open_array
      << "JFK" << "LGA" << "EWR" << close_array
    << close_document
    << "dst_airport" << "BCN";
  std::cout << "query: "<< bsoncxx::to_json(filter.view()) << std::endl;
  std::cout << "NYC -> Barcelona: " << coll.count(filter.view())<< std::endl;
}


void airfrance_destination_NYC(){
  // instantiate a connection
  client conn{mongocxx::uri{}};
  // instantiate a collection
  collection coll = conn["air"]["routes"];

  document filter, projection;
  filter << "airline.name" << "Air France" << "dst_airport" << open_document
    << "$in" << open_array
      << "JFK" << "LGA" << "EWR" << close_array
    << close_document;
  projection << "airplane" << 1 << "_id" << 0;

  options::find opts;
  opts.projection(projection.view());
  std::cout << "query: "<< bsoncxx::to_json(filter.view()) << std::endl;
  cursor c = coll.find(filter.view(), opts);

  for ( auto&& d : c ){
    std::cout << bsoncxx::to_json(d) << std::endl;
  }
}

void lower_than_10(){
  // instantiate a connection
  client conn{mongocxx::uri{}};
  // instantiate a collection
  collection coll = conn["air"]["airlines"];

  document filter;
  filter << "airline" << open_document << "$lt" << 10 << close_document;

  cursor c = coll.find(filter.view());
  std::cout << "Lower than 10" << std::endl;
  for ( auto&& d : c ){
    std::cout << bsoncxx::to_json(d) << std::endl;
  }
}


void italian_or_german_skip5_limit10(){
  // instantiate a connection
  client conn{mongocxx::uri{}};
  // instantiate a collection
  collection coll = conn["air"]["airlines"];

  document filter, german;
  german << "country" << "Germany";

  bsoncxx::types::b_document g{german.view()};

  filter << "$or" << open_array
    << g
    << open_document  << "country" << "Italy" << close_document
  << close_array;

  options::find opts;
  opts.skip(5);
  opts.limit(10);

  cursor c = coll.find(filter.view(), opts);
  std::cout << "italian_or_german_skip5_limit10" << std::endl;
  for ( auto&& d : c ){
    std::cout << bsoncxx::to_json(d) << std::endl;
  }
}

int main(int, char**) {
    try{
      count_spanish_airlines();
      routes_NYC_BARCELONA();
      airfrance_destination_NYC();
      lower_than_10();
      italian_or_german_skip5_limit10();
    } catch( const exception &e ) {
      std::cout << "caught " << e.what() << std::endl;
    }
    return EXIT_SUCCESS;

}
