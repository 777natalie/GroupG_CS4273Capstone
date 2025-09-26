import React, { useState, useEffect } from 'react';
import { useInView } from 'react-intersection-observer';
import styles from "./SummaryDisplaySectionComponent.module.css";

const SummarySection = ({ natureCode, requiredQuestions }) => {
  const [hasAnimated, setHasAnimated] = useState(false);
  const { ref, inView } = useInView({ triggerOnce: true });

  const missedQuestions = requiredQuestions ? requiredQuestions.filter(q => !q.was_asked) : [];
  const totalRequired = requiredQuestions ? requiredQuestions.length : 0;
  const numAsked = totalRequired - missedQuestions.length;
  const completenessPercentage = totalRequired > 0 ? Math.round((numAsked / totalRequired) * 100) : 0;

  useEffect(() => {
    if (inView && !hasAnimated) {
      setHasAnimated(true);
    }
  }, [inView, hasAnimated]);

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <h2 className="text-xl font-semibold text-indigo-700 mb-5 border-b-2 border-indigo-300 pb-2">
        <span role="img" aria-label="clipboard">📋</span> Call Summary
      </h2>

      {natureCode && natureCode.length > 0 && (
        <div className="mb-5">
          <h3 className="text-lg font-medium text-gray-700 mb-3">
            <span role="img" aria-label="label">🏷️</span> Identified Nature Codes/Sections:
          </h3>
          <ul className="list-disc pl-6 space-y-2">
            {natureCode.map((code, index) => (
              <li key={index} className="text-gray-600">
                <span className="font-semibold text-indigo-600">{code.name}:</span>{' '}
                <span className="text-sm italic">{code.explanation}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {missedQuestions.length > 0 && (
        <div className="mb-5">
          <h3 className="text-lg font-medium text-red-700 mb-3">
            <span role="img" aria-label="warning">⚠️</span> Missed Questions:
          </h3>
          <ul className="space-y-3">
            {missedQuestions.map((question, index) => (
              <li key={index} className="flex items-center text-gray-600">
                <span className="inline-block w-4 h-4 rounded-full mr-3 bg-red-500 shadow"></span>
                <span className="text-sm">
                  {index + 1}. {question.text}
                  {question.justification && (
                    <span className="ml-2 text-xs italic text-gray-500">({question.justification})</span>
                  )}
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {totalRequired > 0 && (
        <div ref={ref} className="mt-6">
          <h3 className="text-md font-semibold text-indigo-700 mb-3 text-center">
            <span role="img" aria-label="check-mark">✅</span> Call Completeness:
          </h3>
          <div className="flex flex-col items-center">
            <div className={styles.progressBarContainer}>
              <div
                className={styles.progressBarFill}
                style={{ width: hasAnimated ? `${completenessPercentage}%` : '0%' }}
              >
                {completenessPercentage}%
              </div>
              <div className={styles.progressBarTooltip}>
                <span className={styles.tooltipText}>
                  {numAsked} of {totalRequired} questions answered
                </span>
              </div>
            </div>
            <p className="mt-2 text-sm text-gray-600 text-center">
              {completenessPercentage === 100 ? (
                <span className="text-green-500 font-bold">All required questions were asked.</span>
              ) : (
                <span className="text-orange-500 font-bold">Some questions were missed.</span>
              )}
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default SummarySection;