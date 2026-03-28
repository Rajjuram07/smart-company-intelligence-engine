import React from 'react';

const CompanyCard = ({ data }) => {
    if (!data) return null;

    return (
        <div className="w-full bg-white rounded-2xl shadow-xl overflow-hidden border border-slate-100 flex flex-col gap-6 animate-fade-in pb-8">
            {/* Header */}
            <div className="bg-gradient-to-r from-blue-600 to-indigo-700 p-8 text-white relative">
                <div className="flex justify-between items-start">
                    <div>
                        <h2 className="text-3xl font-bold mb-2">{data.company_name}</h2>
                        <div className="flex gap-4 text-blue-100 text-sm font-medium">
                            {data.company_type && <span>{data.company_type}</span>}
                            {data.founded_year && <span>Est. {data.founded_year}</span>}
                            {data.location && <span>📍 {data.location}</span>}
                        </div>
                    </div>
                    <div className="flex flex-col items-center bg-white/10 backdrop-blur-md rounded-xl p-3 border border-white/20">
                        <span className="text-xs uppercase tracking-wider font-semibold opacity-90 mb-1">Trust Score</span>
                        <div className="text-3xl font-black">{data.trust_score}</div>
                    </div>
                </div>

                <div className="absolute -bottom-4 left-8 bg-blue-50 text-blue-900 border border-blue-200 px-4 py-1.5 rounded-full text-sm font-bold shadow-sm">
                    Status: {data.legitimacy_status}
                </div>
            </div>

            <div className="px-8 mt-4 grid grid-cols-1 md:grid-cols-2 gap-8">
                {/* Left Column */}
                <div className="space-y-8">
                    {/* AI Summary */}
                    <section>
                        <h3 className="text-lg font-bold text-slate-800 mb-3 flex items-center gap-2">
                            <span className="text-indigo-600">✨</span> AI Summary
                        </h3>
                        <p className="text-slate-600 leading-relaxed text-base bg-slate-50 p-4 rounded-xl border border-slate-100">
                            {data.ai_summary}
                        </p>
                    </section>

                    {/* Official Links */}
                    <section>
                        <h3 className="text-lg font-bold text-slate-800 mb-3 flex items-center gap-2">
                            <span className="text-blue-500">🔗</span> Important Links
                        </h3>
                        <div className="flex flex-col gap-3">
                            {data.website && (
                                <a href={data.website} target="_blank" rel="noreferrer" className="flex items-center gap-3 p-3 rounded-lg border border-slate-200 hover:border-blue-400 hover:bg-blue-50 transition-all text-slate-700 hover:text-blue-700 font-medium font-sans">
                                    🌐 Official Website
                                </a>
                            )}
                            {data.linkedin && (
                                <a href={data.linkedin} target="_blank" rel="noreferrer" className="flex items-center gap-3 p-3 rounded-lg border border-slate-200 hover:border-blue-400 hover:bg-blue-50 transition-all text-slate-700 hover:text-blue-700 font-medium font-sans">
                                    💼 LinkedIn Profile
                                </a>
                            )}
                        </div>
                    </section>
                </div>

                {/* Right Column */}
                <div className="space-y-8">
                    {/* Recent Jobs */}
                    {data.jobs && data.jobs.length > 0 && (
                        <section>
                            <h3 className="text-lg font-bold text-slate-800 mb-3 flex items-center gap-2">
                                <span className="text-emerald-500">📌</span> Recent Jobs
                            </h3>
                            <div className="flex flex-col gap-3">
                                {data.jobs.map((job, idx) => (
                                    <a key={idx} href={job.url} target="_blank" rel="noreferrer" className="block p-3 rounded-lg border border-slate-200 bg-white hover:border-emerald-400 hover:shadow-md transition-all group">
                                        <div className="font-semibold text-slate-800 group-hover:text-emerald-700 truncate">{job.title}</div>
                                        <div className="flex justify-between text-xs text-slate-500 mt-1">
                                            <span>{job.platform}</span>
                                            <span>{job.location}</span>
                                        </div>
                                    </a>
                                ))}
                            </div>
                        </section>
                    )}

                    {/* Reviews Summary */}
                    {data.reviews && data.reviews.length > 0 && (
                        <section>
                            <h3 className="text-lg font-bold text-slate-800 mb-3 flex items-center gap-2">
                                <span className="text-amber-500">⭐</span> Ratings & Reviews
                            </h3>
                            <div className="grid gap-3">
                                {data.reviews.map((review, idx) => (
                                    <div key={idx} className="p-4 rounded-lg bg-orange-50 border border-orange-100 flex flex-col gap-2">
                                        <div className="flex justify-between items-center">
                                            <span className="font-bold text-slate-800 text-sm">{review.platform}</span>
                                            {review.rating && (
                                                <span className="bg-white px-2 py-0.5 rounded text-xs font-bold text-amber-600 border border-amber-200">
                                                    {review.rating}
                                                </span>
                                            )}
                                        </div>
                                        <p className="text-slate-600 text-sm italic">"{review.summary}"</p>
                                    </div>
                                ))}
                            </div>
                        </section>
                    )}
                </div>
            </div>

            {/* Sources footer */}
            {data.source_links && data.source_links.length > 0 && (
                <div className="px-8 mt-4 pt-6 border-t border-slate-100">
                    <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Sources Examined</h4>
                    <div className="flex flex-wrap gap-2">
                        {data.source_links.map((link, idx) => (
                            <a key={idx} href={link.url} target="_blank" rel="noreferrer" className="text-xs bg-slate-100 text-slate-600 px-3 py-1.5 rounded-full hover:bg-slate-200 transition-colors max-w-[200px] truncate">
                                {link.title || link.url}
                            </a>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default CompanyCard;
