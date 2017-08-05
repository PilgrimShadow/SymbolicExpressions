#AUTH: Jordan Dodson

#TODO (x == complete | . == in progress | - == canceled)
# (.) _simplify() for Add class
# ( ) _simplify() for Mult class
# (x) Write a Const class
# ( ) Neg function or use a special method
# ( ) simplify on initialization
# ( ) Write a static .parse() method
# ( ) Introduce basic trig functions
# ( ) Write __str__() methods for all classes
# ( ) Consider using __new__ to handle corner-cases in simplification (i.e. Mult(1, 'x'))

class Expression():
  '''The base class for all symbolic expressions'''

  def __init__(self):
    # The set of labels in this expression
    self.labels = set()

  # Unary operations

  def __pos__(self):
    return self

  def __neg__(self):
    return self.neg()

  def __add__(self, other):
    return Add(self, other)

  def __radd__(self, other):
    return Add(self, other)

  def __mul__(self, other):
    return Mult(self, other)

  def __rmul__(self, other):
    return Mult(self, other)

  def neg(self):
    pass

  def deriv(self, wrt):
    pass

  def integral(self, wrt):
    pass

  def evaluate(self, value_dict):
    pass

  def _simplify(self):
    pass


class Const(Expression):

  def __init__(self, value):
    self.labels = set()
    self.value = value

  def neg(self):
    return Const(-self.value)

  def evaluate(self, **value_dict):
    return self

  def deriv(self, wrt):
    return Const(0)

  def __str__(self):
    return str(self.value)

  def __repr__(self):
    return 'Const({})'.format(self.value)


class Symbol(Expression):
  '''Represents a single symbol'''

  def __init__(self, label):

    self.labels = set([label])

    if isinstance(label, str) and label.isalpha():
      self.label = label
    else:
      raise Exception('Invalid symbol label')

  def neg(self):
    return Mult(Const(-1), self)

  def evaluate(self, **value_dict):
    if self.label in value_dict:
      return Const(value_dict[self.label])
    else:
      return self

  def deriv(self, wrt):
    return Const(1) if self.label == wrt else Const(0)

  def __str__(self):
    return self.label

  def __repr__(self):
    return 'Symbol({:s})'.format(self.label)


class Add(Expression):
  '''Represents the addition of two or more sub-expressions'''

  def __init__(self, a, b, *rest):

    self.terms = [a,b] + list(rest)

    self._simplify()


  def evaluate(self, **value_dict):
    z = [term.evaluate(value_dict) for term in self.terms]
    return Add(*z)

  def deriv(self, wrt):

    if wrt in self.labels:
      z = [term.deriv(wrt) for term in self.terms]
      return Add(*z)
    else:
      return Const(0)

  def _get_labels(self):

    labels = set()

    for term in self.terms:
      labels.update(term.labels)

    return labels
    

  def _simplify(self):

    # List of sub-expressions to check
    to_check = self.terms.copy()
    simplified = []
    counts = {}
    offset = 0

    for expr in to_check:
      if isinstance(expr, Const):
        offset += expr.value
      elif isinstance(expr, Symbol):
        counts[expr.label] = 1 + counts.get(expr.label, 0)
      elif isinstance(expr, Add):
        to_check.extend(expr.terms)
      else:
        simplified.append(expr)

    # Group symbols together
    for label, count in counts.items():
      simplified.append(Mult(Const(count), Symbol(label)) if count > 1 else Symbol(label))

    # Add the offset term
    if offset != 0:
      simplified.append(Const(offset))

    # The simplified terms of this Add
    self.terms = simplified

    # Recompute the set of labels in this Expression
    self.labels = self._get_labels()

  def __str__(self):
    return ' + '.join(str(term) for term in self.terms)

  def __repr__(self):
    return 'Add({:s})'.format(', '.join(repr(term) for term in self.terms))
      

class Mult(Expression):
  '''Represents the product of two or more sub-expressions'''

  def __init__(self, a, b, *rest):
    self.terms = [a,b] + list(rest)

    self.labels = set()
    for term in self.terms:
      if isinstance(term, Expression):
        self.labels.update(term.labels)

  def neg(self):
    return Mult(Const(-1), self)

  def _simplify(self):
    pass

  def __str__(self):
    return ''.join(str(term) for term in self.terms)

  def __repr__(self):
    return 'Mult({:s})'.format(', '.join(repr(term) for term in self.terms))


class Exp(Expression):

  def __init__(self):
    pass
