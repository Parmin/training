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




void update_airlines(document &filter, document &update){

  client conn{mongocxx::uri{}};
  // instantiate a collection
  collection coll = conn["air"]["airlines"];

  auto res = coll.update_many(filter.view(), update.view());
  std::cout << "result" << std::endl
  << " modif "<< res->modified_count() << std::endl
  << " matched "<< res->matched_count() << std::endl;
}

void update_90(){

  document filter, update;
  filter << "name" << open_document
    << "$in" << open_array
      << "Emirates" << "Qatar Airways" << close_array
    << close_document;

  update << "$set" << open_document
    << "points" << 90 << close_document;

  update_airlines(filter, update);
}

void update_75(){
  document filter, update;

  filter << "$or" << open_array
      << open_document << "name"<< "Iberia Airlines" << close_document
      << open_document << "name"<<  "Air France" << close_document
    << close_array;

  update << "$set" << open_document
    << "points" << 75 << close_document;

  update_airlines(filter, update);
}

void update_50(){
  document update, filter;
  filter << "points" << open_document
    << "$exists" << false
  << close_document;

  update << "$set" << open_document
    << "points" << 50 << close_document;
  update_airlines(filter, update);
}

void inc_portuguese(){
  document update, filter;
  filter << "country" << "Portugal";
  update << "$inc" << open_document
    << "points" << 10 << close_document;

  update_airlines(filter, update);
}


void update_bookings(){
  client conn{mongocxx::uri{}};
  // instantiate a collection
  collection coll = conn["air"]["bookings"];

  document update, filter;
  filter << "dst_airport" << "JFK" << "src_airport" << "LHR";
  update << "$inc" << open_document
    << "bookingPast7Days.4" << 200 << close_document;

  coll.update_one(filter.view(), update.view());
}

int main(int, char**) {
    try{
      update_90();
      update_75();
      update_50();
      inc_portuguese();
      update_bookings();
    } catch( const exception &e ) {
      std::cout << "caught " << e.what() << std::endl;
    }
    return EXIT_SUCCESS;
}
