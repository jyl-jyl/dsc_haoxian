package datalog

sealed abstract class Aggregator {
  def literal: Literal
  def aggParam: Parameter
  def aggResult: Parameter
  def relation: Relation = literal.relation
  require(literal.fields.contains(aggParam))
  require(!literal.fields.contains(aggResult))
}

case class Sum(literal: Literal, aggParam: Variable, aggResult: Variable) extends Aggregator {
  override def toString: String = s"$aggResult = sum $aggParam: $literal"
}
