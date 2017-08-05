#AUTH: Jordan Dodson

#TODO (x == complete | . == in progress | - == canceled)
# (.) _simplified() for Add class
# ( ) _simplified() for Mult class
# (x) Write a Const class
# ( ) Neg function or use a special method
# ( ) simplify on initialization

class Expression():
  '''The base class for all symbolic expressions'''

  def __init__(self):
    # The set of labels in this expression
    self.labels = set()

  def __add__(self, other):
    z = Add(self, other)
    return z._simplified()

  def __mul__(self, other):
    z = Mult(self, other)
    return z._simplified()

  def deriv(self, wrt=None):
    pass

  def integral(self, wrt=None):
    pass

  def evaluate(self, value_dict):
    pass

  def _simplified(self):
    pass


class Const(Expression):

  def __init__(self, value):
    self.labels = set()
    self.value = value

  def evaluate(self, value_dict):
    return self

  def _simplified(self):
    return self

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

   def evaluate(self, value_dict):
     return value_dict.get(self.label, self)

   def __repr__(self):
     return 'Symbol({:s})'.format(self.label)


class Add(Expression):
  '''Represents the addition of two or more sub-expressions'''

  def __init__(self, a, b, *rest):

    self.terms = [a,b] + list(rest)

    # Get the set of labels in this Expression
    self.labels = set()
    for term in self.terms:
      if isinstance(term, Expression):
        self.labels.update(term.labels)

  def evaluate(self, value_dict):
    z = [term.evaluate(value_dict) for term in self.terms]
    return Add(*z)._simplified()

  def _simplified(self):

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

    return Add(*simplified) if len(simplified) > 1 else simplified[0]

  def __repr__(self):
    return 'Add({:s})'.format(', '.join(str(term) for term in self.terms))
      

class Mult(Expression):
  '''Represents the product of two or more sub-expressions'''

  def __init__(self, a, b, *rest):
    self.terms = [a,b] + list(rest)

    self.labels = set()
    for term in self.terms:
      if isinstance(term, Expression):
        self.labels.update(term.labels)

  def _simplified(self):
    pass

  def __repr__(self):
    return 'Mult({:s})'.format(', '.join(str(term) for term in self.terms))


class Exp(Expression):

  def __init__(self):
    pass
